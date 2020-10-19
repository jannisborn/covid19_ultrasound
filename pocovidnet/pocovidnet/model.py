#POCOVID-Net model.
import tensorflow as tf
from tensorflow.keras.applications import (
    VGG16, MobileNetV2, NASNetMobile, ResNet50
)
from tensorflow.keras.layers import (
    AveragePooling2D,
    Dense,
    Dropout,
    Flatten,
    Input,
    BatchNormalization,
    ReLU,
    LeakyReLU
)
from tensorflow.keras.models import Model
from pocovidnet.layers import global_average_pooling
from .utils import fix_layers


def get_model(
    input_size: tuple = (224, 224, 3),
    hidden_size: int = 64,
    dropout: float = 0.5,
    num_classes: int = 3,
    trainable_layers: int = 1,
    log_softmax: bool = True,
    mc_dropout: bool = False,
    **kwargs
):
    act_fn = tf.nn.softmax if not log_softmax else tf.nn.log_softmax

    # load the VGG16 network, ensuring the head FC layer sets are left off
    baseModel = VGG16(
        weights="imagenet",
        include_top=False,
        input_tensor=Input(shape=input_size)
    )
    # construct the head of the model that will be placed on top of the
    # the base model
    headModel = baseModel.output
    headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
    headModel = Flatten(name="flatten")(headModel)
    headModel = Dense(hidden_size)(headModel)
    headModel = BatchNormalization()(headModel)
    headModel = ReLU()(headModel)
    headModel = (
        Dropout(dropout)(headModel, training=True)
        if mc_dropout else Dropout(dropout)(headModel)
    )
    headModel = Dense(num_classes, activation=act_fn)(headModel)

    # place the head FC model on top of the base model
    model = Model(inputs=baseModel.input, outputs=headModel)

    model = fix_layers(model, num_flex_layers=trainable_layers + 8)

    return model


def get_cam_model(
    input_size: tuple = (224, 224, 3),
    num_classes: int = 3,
    trainable_layers: int = 1,
    dropout: float = 0.5,
    log_softmax: bool = False,
    mc_dropout: bool = False,
    *args,
    **kwargs
):
    """
    Get a VGG model that supports class activation maps w/o guided gradients

    Keyword Arguments:
        input_size {tuple} -- [Image size] (default: {(224, 224, 3)})
        num_classes {int} -- [Number of output classes] (default: {3})
        trainable_layers {int} -- [Number of trainable layers] (default: {3})

    Returns:
        tensorflow.keras.models object
    """
    act_fn = tf.nn.softmax if not log_softmax else tf.nn.log_softmax

    # load the VGG16 network, ensuring the head FC layer sets are left off
    baseModel = VGG16(
        weights="imagenet",
        include_top=False,
        input_tensor=Input(shape=input_size)
    )
    headModel = baseModel.output
    headModel = global_average_pooling(headModel)
    headModel = (
        Dropout(dropout)(headModel, training=True)
        if mc_dropout else Dropout(dropout)(headModel)
    )
    headModel = Dense(num_classes, activation=act_fn)(headModel)

    model = Model(inputs=baseModel.input, outputs=headModel)
    model = fix_layers(model, num_flex_layers=trainable_layers + 2)

    return model


def get_mobilenet_v2_model(
    input_size: tuple = (224, 224, 3),
    hidden_size: int = 64,
    dropout: float = 0.5,
    num_classes: int = 3,
    trainable_layers: int = 0,
    log_softmax: bool = False,
    **kwargs
):
    """Get a MobileNetV2 model

    Keyword Arguments:
        input_size {tuple} -- [size of input images] (default: {(224, 224, 3)})
        hidden_size {int} -- [description] (default: {64})
        dropout {float} -- [description] (default: {0.5})
        num_classes {int} -- [description] (default: {3})
        trainable_layers {int} -- [description] (default: {0})
        log_softmax {bool} -- [description] (default: {False})

    Returns:
        [type] -- [description]
    """
    act_fn = tf.nn.softmax if not log_softmax else tf.nn.log_softmax

    # load the VGG16 network, ensuring the head FC layer sets are left off
    baseModel = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_tensor=Input(shape=input_size)
    )
    # construct the head of the model that will be placed on top of the
    # the base model
    headModel = baseModel.output
    headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
    headModel = Flatten(name="flatten")(headModel)
    headModel = Dense(hidden_size)(headModel)
    headModel = BatchNormalization()(headModel)
    headModel = ReLU()(headModel)
    headModel = Dropout(dropout)(headModel)
    headModel = Dense(num_classes, activation=act_fn)(headModel)

    # place the head FC model on top of the base model
    model = Model(inputs=baseModel.input, outputs=headModel)

    model = fix_layers(model, num_flex_layers=trainable_layers + 8)

    return model


def get_nasnet_model(
    input_size: tuple = (224, 224, 3),
    hidden_size: int = 512,
    dropout: float = 0.5,
    num_classes: int = 3,
    trainable_layers: int = 0,
    log_softmax: bool = False,
    **kwargs
):
    """Get a NasNet model

    Keyword Arguments:
        input_size {tuple} -- [size of input images] (default: {(224, 224, 3)})
        hidden_size {int} -- [description] (default: {64})
        dropout {float} -- [description] (default: {0.5})
        num_classes {int} -- [description] (default: {3})
        trainable_layers {int} -- [description] (default: {0})
        log_softmax {bool} -- [description] (default: {False})

    Returns:
        [type] -- [description]
    """
    act_fn = tf.nn.softmax if not log_softmax else tf.nn.log_softmax

    baseModel = NASNetMobile(
        weights="imagenet",
        include_top=False,
        input_tensor=Input(shape=input_size)
    )
    # construct the head of the model that will be placed on top of the
    # the base model
    headModel = baseModel.output
    headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
    headModel = Flatten(name="flatten")(headModel)
    headModel = Dense(hidden_size)(headModel)
    headModel = ReLU()(headModel)
    headModel = Dropout(dropout)(headModel)
    headModel = BatchNormalization()(headModel)
    headModel = Dense(num_classes, activation=act_fn)(headModel)

    # place the head FC model on top of the base model
    model = Model(inputs=baseModel.input, outputs=headModel)

    model = fix_layers(model, num_flex_layers=trainable_layers + 8)

    return model


def get_dense_model(
    input_size: int = 640,
    hidden_sizes: list = [512, 256],
    dropout: float = 0.5,
    num_classes: int = 4,
    batch_norm: bool = True,
    log_softmax: bool = False,
    **kwargs
):
    """Get a NasNet model

    Keyword Arguments:
        input_size {tuple} -- [size of input images] (default: {(224, 224, 3)})
        hidden_size {int} -- [description] (default: {64})
        dropout {float} -- [description] (default: {0.5})
        num_classes {int} -- [description] (default: {3})
        trainable_layers {int} -- [description] (default: {0})
        log_softmax {bool} -- [description] (default: {False})

    Returns:
        [type] -- [description]
    """
    out_fn = tf.nn.softmax if not log_softmax else tf.nn.log_softmax

    # construct the head of the model that will be placed on top of the
    # the base model

    inputs = tf.keras.Input(shape=(input_size, ))
    inter = inputs

    for hidden_size in hidden_sizes:
        inter = Dense(hidden_size)(inter)
        if batch_norm:
            inter = BatchNormalization()(inter)
        inter = LeakyReLU()(inter)
        if dropout > 0.:
            inter = Dropout(dropout)(inter)

    outputs = Dense(num_classes, activation=out_fn)(inter)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)

    return model


def get_resnet50_model(
    input_size: tuple = (224, 224, 3),
    hidden_size: int = 64,
    dropout: float = 0.5,
    num_classes: int = 3,
    trainable_layers: int = 3,
    log_softmax: bool = True,
    mc_dropout: bool = False,
    **kwargs
):
    act_fn = tf.nn.softmax if not log_softmax else tf.nn.log_softmax

    # load the VGG16 network, ensuring the head FC layer sets are left off
    baseModel = ResNet50(
        weights="imagenet",
        include_top=False,
        input_tensor=Input(shape=input_size)
    )
    # construct the head of the model that will be placed on top of the
    # the base model
    headModel = baseModel.output
    headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
    headModel = Flatten(name="flatten")(headModel)
    headModel = Dense(hidden_size)(headModel)
    headModel = BatchNormalization()(headModel)
    headModel = ReLU()(headModel)
    headModel = (
        Dropout(dropout)(headModel, training=True)
        if mc_dropout else Dropout(dropout)(headModel)
    )
    headModel = Dense(num_classes, activation=act_fn)(headModel)

    # place the head FC model on top of the base model
    model = Model(inputs=baseModel.input, outputs=headModel)

    model = fix_layers(model, num_flex_layers=trainable_layers + 8)

    return model