import shutil
from roboflow import Roboflow

rf = Roboflow(api_key="AxO5yv9cBEGsHgZUq7sB")
project = rf.workspace("testworkspace-7jvng").project("license-plate-detection-itypr")
version = project.version(9)
dataset = version.download("coco-mmdetection")

shutil.move('license-plate-detection-9/', 'data/license-plate-detection-9/')