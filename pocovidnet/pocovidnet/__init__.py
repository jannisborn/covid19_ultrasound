from .model import (
    get_cam_model, get_model, get_mobilenet_v2_model, get_nasnet_model
)

MODEL_FACTORY = {
    'vgg_base': get_model,
    'vgg_cam': get_cam_model,
    'mobilenet_v2': get_mobilenet_v2_model,
    'nasnet': get_nasnet_model
}
