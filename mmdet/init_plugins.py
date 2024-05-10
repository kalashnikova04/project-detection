# Copyright (c) OpenMMLab. All rights reserved.
import os

from mmdeploy.utils import get_file_path


def get_ops_path() -> str:
    """Get the library path of onnxruntime custom ops.

    Returns:
        str: The library path to onnxruntime custom ops.
    """
    candidates = [
        '../../../build/lib/libmmdeploy_onnxruntime_ops.so',
        '../../lib/libmmdeploy_onnxruntime_ops.so',
        '../deploy_workspace/mmdeploy/build/lib/mmdeploy_onnxruntime_ops.dll'
    ]
    return get_file_path(os.path.dirname(__file__), candidates)


def get_lib_path() -> str:
    """Get the library path of onnxruntime.

    Returns:
        str: The library path to onnxruntime.
    """
    candidates = [
        '../../../../onnxruntime-linux-x64-1.12.0/lib/libonnxruntime.so*',
        '../../lib/libonnxruntime.so*',
        '../../lib/onnxruntime.dll',
    ]
    return get_file_path(os.path.dirname(__file__), candidates)