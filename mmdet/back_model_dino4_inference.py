# import os
from mmdeploy.apis.utils import build_task_processor
from mmdeploy.utils import get_input_shape, load_config, get_root_logger
import torch
# import onnxruntime as ort
# from mmdet.init_plugins import get_ops_path


def backend_model_inference(
        image,
        deploy_cfg = '../deploy_workspace/mmdeploy/configs/mmdet/detection/detection_onnxruntime_dynamic.py',
        model_cfg = 'configs/dino/dino-4scale_r50_1xb2-12e_lp.py',
        backend_model = ['mmdeploy_models/mmdet/onnx/end2end.onnx'],
        device = 'cpu'
):
    image_name = image.name

    deploy_cfg, model_cfg = load_config(deploy_cfg, model_cfg)

    task_processor = build_task_processor(model_cfg, deploy_cfg, device)
    model = task_processor.build_backend_model(backend_model)

    input_shape = get_input_shape(deploy_cfg)
    model_inputs, _ = task_processor.create_input(image, input_shape)

    with torch.no_grad():
        result = model.test_step(model_inputs)

    print(result)

    task_processor.visualize(
        image=image,
        model=model,
        result=result[0],
        window_name='visualize',
        output_file=f'share_web/preds/out_det_{image_name}.png')
