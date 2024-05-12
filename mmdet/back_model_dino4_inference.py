import os
from mmdeploy.apis.utils import build_task_processor
from mmdeploy.utils import get_input_shape, load_config
import torch
import json

import pika
from uuid import uuid4
from dotenv import load_dotenv
import psycopg2
from db_communication import update_task


load_dotenv()
RMQ_URL = os.getenv('RMQ_URL')
QUEUE_NAME = os.environ.get('QUEUE_NAME', 'test_direct')
EXCHANGE_NAME = os.environ.get('EXCHANGE_NAME', 'to_direct')
PREFETCH_COUNT = 3


def main():
    worker_id = uuid4().hex[:4]

    connection = pika.BlockingConnection(pika.URLParameters(RMQ_URL))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout", durable=True)

    channel.queue_declare(queue=f'{QUEUE_NAME}_rejected', durable=True)
    channel.queue_declare(queue=QUEUE_NAME, durable=True,
                          arguments={'x-dead-letter-exchange': '',
                                     'x-dead-letter-routing-key': f'{QUEUE_NAME}_rejected'})

    channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key='direct_out')
    channel.basic_qos(prefetch_count=PREFETCH_COUNT)

    def backend_model_inference(
            images,
            deploy_cfg = '../deploy_workspace/mmdeploy/configs/mmdet/detection/detection_onnxruntime_dynamic.py',
            model_cfg = 'configs/dino/dino-4scale_r50_1xb2-12e_lp.py',
            backend_model = ['mmdeploy_models/mmdet/onnx/end2end.onnx'],
            # ['share_web/end2end.onnx'],
            device = 'cpu'
    ):
        
        images = ['share_web/uploads/' + image for image in images]

        deploy_cfg, model_cfg = load_config(deploy_cfg, model_cfg)

        task_processor = build_task_processor(model_cfg, deploy_cfg, device)
        model = task_processor.build_backend_model(backend_model)

        input_shape = get_input_shape(deploy_cfg)

        for image in images:
            model_inputs, _ = task_processor.create_input(image, input_shape)

            with torch.no_grad():
                result = model.test_step(model_inputs)


            task_processor.visualize(
                image=image,
                model=model,
                result=result[0],
                window_name='visualize',
                output_file=f'share_web/preds/out_det_{os.path.split(image)[1]}.png')
    
    def callback(ch, method, properties, body):
        data = json.loads(body)
        task_num = data.get('task_id')
        print(f">>> start processing message {task_num}")

        conn_db = psycopg2.connect(
            database="postgres",
            host=os.getenv('POSTGRES_HOST'),
            user=os.getenv('PGUSER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        try:
            update_task(conn_db, task_num, 'IN_PROGRESS', worker_id)
            images = data.get('images')
            backend_model_inference(images)

            ch.basic_ack(delivery_tag=method.delivery_tag)

            update_task(conn_db, task_num, 'DONE', worker_id)

            print(f"<<< end processing message {task_num}")
        except Exception as ex:
            print(f"Error occurred: {ex}")
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

            update_task(conn_db, task_num, 'ERROR', worker_id)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False, consumer_tag=worker_id)
    channel.start_consuming()


if __name__ == '__main__':
    main()
