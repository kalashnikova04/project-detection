import os
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from .forms import ImageForm
# from media.back_model_dino4_inference import backend_model_inference
import pika
import json

from main.models import Task


RMQ_URL = os.getenv('RMQ_URL')
QUEUE_NAME = os.environ.get('QUEUE_NAME', 'test_direct')
EXCHANGE_NAME = os.environ.get('EXCHANGE_NAME', 'to_direct')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


def index(request):
    # if os.path.exists('model.pickle') and os.path.exists('data.npz'):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img = form.instance
            print(img, type(img))
            context = {'form': form, 'img': img, 'img_title': img.image.url[15:]}
            return render(request, 'main/index.html', context=context)
    else:
        form = ImageForm()
        return render(request, 'main/index.html', {'form': form})
    # return render(request, 'main/need_train.html')


def train_yolo(request):
    return


def send_inference_task(request):
    try:
        img = request.GET.get('image')
    # print(type(img), img.size, type(img.name), type(img.field_name))
    except Exception as e:
        print(e)
        return render(request, 'main/error.html')
    
    routing_key = ''
    worker_id = 'Unknown'

    request.session['images'] = [img]
    
    
    with pika.BlockingConnection(pika.URLParameters(RMQ_URL)) as connection:
        with connection.channel() as channel:

            task = Task(status='PENDING', worker_id=worker_id, mode='inference')
            task.save()
            task_num = task.id
            time_created = task.time
            data = {'images': [img],
                    'routing_key': routing_key,
                    'mode': 'train',
                    'task_id': task_num,
                    'time_created': time_created}

            channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout", durable=True)
            channel.queue_declare(queue=f'{QUEUE_NAME}_rejected', durable=True)
            channel.queue_declare(queue=QUEUE_NAME, durable=True,
                                arguments={'x-dead-letter-exchange': '',
                                            'x-dead-letter-routing-key': f'{QUEUE_NAME}_rejected'})
            channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key='direct_out')


            channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=routing_key, body=json.dumps(data, cls=DjangoJSONEncoder).encode())

    context = {
        'task_num': task_num,
        'mode': 'train'}

    return render(request, 'main/mode.html', context)


async def update_task_status(request):
    print("[update_task_status]")
    tasks = [task async for task in Task.objects.all()]
    context = {'tasks': tasks}
    return render(request, 'main/tasks.html', context)


def get_prediction(request):
    images = request.session.get('images')
    context = {'images': images}
    return render(request, 'main/get_predicted.html', context)
