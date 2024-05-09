ARG PYTORCH="1.9.0"
ARG CUDA="11.1"
ARG CUDNN="8"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

ENV TORCH_CUDA_ARCH_LIST="6.0 6.1 7.0 7.5 8.0 8.6+PTX" \
    TORCH_NVCC_FLAGS="-Xfatbin -compress-all" \
    CMAKE_PREFIX_PATH="$(dirname $(which conda))/../" \
    FORCE_CUDA="1"

# Avoid Public GPG key error
# https://github.com/NVIDIA/nvidia-docker/issues/1631
RUN rm /etc/apt/sources.list.d/cuda.list \
    && rm /etc/apt/sources.list.d/nvidia-ml.list \
    && apt-key del 7fa2af80 \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

# (Optional, use Mirror to speed up downloads)
# RUN sed -i 's/http:\/\/archive.ubuntu.com\/ubuntu\//http:\/\/mirrors.aliyun.com\/ubuntu\//g' /etc/apt/sources.list && \
#    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Install the required packages
RUN apt-get update \
    && apt-get install -y ffmpeg libsm6 libxext6 git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install MMEngine and MMCV
RUN pip install openmim && \
    mim install "mmengine>=0.7.1" "mmcv>=2.0.0rc4, <2.2.0"

# Install MMDetection
RUN conda clean --all \
    && git clone https://github.com/open-mmlab/mmdetection.git /mmdetection \
    && cd /mmdetection \
    && pip install --no-cache-dir -e .

RUN pip install -r /mmdetection/requirements/albu.txt && \
    pip install -r /mmdetection/requirements/docs.txt && \
    pip install -r /mmdetection/requirements/runtime.txt && \
    pip install -r /mmdetection/requirements/tests.txt && \
    pip install -r /mmdetection/requirements/tracking.txt

ADD requirements.txt /mmdetection

WORKDIR /mmdetection

RUN pip install -r requirements.txt

COPY . /mmdetection

# COPY cfg.py /mmdetection/configs/dcn

# RUN rm /opt/conda/lib/python3.10/site-packages/mmcv/ops/multi_scale_deform_attn.py
# COPY configs/multi_scale_deform_attn.py /opt/conda/lib/python3.10/site-packages/mmcv/ops/multi_scale_deform_attn.py

# RUN rm /mmdetection/mmdet/models/layers/transformer/detr_layers.py
# COPY configs/detr_layers.py /mmdetection/mmdet/models/layers/transformer/detr_layers.py

# RUN rm /mmdetection/mmdet/models/layers/transformer/dino_layers.py
# COPY configs/dino_layers.py /mmdetection/mmdet/models/layers/transformer/dino_layers.py

# RUN rm /mmdetection/mmdet/models/detectors/dino.py
# COPY configs/dino.py /mmdetection/mmdet/models/detectors/dino.py

COPY configs/dino-4scale_r50_1xb2-12e_lp.py /mmdetection/configs/dino
COPY configs/dino-5scale_swin-l_1xb16-12e_lp9.py /mmdetection/configs/dino

WORKDIR /mmdetection
