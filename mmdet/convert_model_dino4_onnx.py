# import os
from mmdeploy.apis import torch2onnx
# from mmdeploy.utils import get_root_logger

# import onnxruntime as ort
# from mmdet.init_plugins import get_ops_path

# ort_custom_op_path = get_ops_path()
# session_options = ort.SessionOptions()

# logger = get_root_logger()
# if os.path.exists(ort_custom_op_path):
#     session_options.register_custom_ops_library(ort_custom_op_path)
#     logger.info('Successfully loaded onnxruntime custom ops from '
#                         f'{ort_custom_op_path}')
# else:
#     logger.warning('The library of onnxruntime custom ops does'
#                     f'not exist: {ort_custom_op_path}')

img = 'demo/demo.jpg'
work_dir = 'mmdeploy_models/mmdet/onnx'
save_file = 'end2end.onnx'
deploy_cfg = '../deploy_workspace/mmdeploy/configs/mmdet/detection/detection_onnxruntime_dynamic.py'
model_cfg = 'configs/dino/dino-4scale_r50_1xb2-12e_lp.py'
model_checkpoint = 'data/dino/epoch_7.pth'
device = 'cpu'

torch2onnx(img, work_dir, save_file, deploy_cfg, model_cfg, model_checkpoint, device)
