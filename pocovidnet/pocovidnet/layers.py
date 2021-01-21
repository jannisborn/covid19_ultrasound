import tensorflow.keras as K


def global_average_pooling(x):
    return K.backend.mean(x, axis=(1, 2))


def global_average_pooling_shape(input_shape):
    return input_shape[0:2]
