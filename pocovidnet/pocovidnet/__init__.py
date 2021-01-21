from .model import (
    get_cam_model, get_model, get_mobilenet_v2_model, get_nasnet_model,
    get_dense_model, get_resnet50_model
)
from .video_model import get_video_model
from .unet3d_genesis import unet_model_3d

MODEL_FACTORY = {
    'vgg_base': get_model,
    'vgg_cam': get_cam_model,
    'mobilenet_v2': get_mobilenet_v2_model,
    'nasnet': get_nasnet_model,
    'dense': get_dense_model,
    'resnet50': get_resnet50_model
}

VIDEO_MODEL_FACTORY = {'base': get_video_model, 'genesis': unet_model_3d}
