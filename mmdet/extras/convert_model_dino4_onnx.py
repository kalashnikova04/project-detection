from mmdeploy.apis import torch2onnx

img = "demo/demo.jpg"
work_dir = "mmdeploy_models/mmdet/onnx"
save_file = "end2end.onnx"
deploy_cfg = "../deploy_workspace/mmdeploy/configs/mmdet/detection/detection_onnxruntime_dynamic.py"
model_cfg = "configs/dino/dino-4scale_r50_1xb2-12e_lp.py"
model_checkpoint = "data/dino/epoch_7.pth"
device = "cpu"

torch2onnx(img, work_dir, save_file, deploy_cfg, model_cfg, model_checkpoint, device)
