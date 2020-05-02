from .model import get_cam_model, get_model

MODEL_FACTORY = {'vgg_base': get_model, 'vgg_cam': get_cam_model}
