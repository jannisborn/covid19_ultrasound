
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import (
    AveragePooling2D, Dense, Dropout, Flatten, Input, BatchNormalization, ReLU
)
from tensorflow.keras.models import Model


def get_model():

    # load the VGG16 network, ensuring the head FC layer sets are left off
    baseModel = VGG16(
        weights="imagenet",
        include_top=False,
        input_tensor=Input(shape=(224, 224, 3))

    )
    # construct the head of the model that will be placed on top of the
    # the base model
    headModel = baseModel.output
    headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
    headModel = Flatten(name="flatten")(headModel)
    headModel = Dense(64)(headModel)
    headModel = BatchNormalization()(headModel)
    headModel = ReLU()(headModel)
    headModel = Dropout(0.5)(headModel)
    headModel = Dense(3, activation="softmax")(headModel)

    # place the head FC model on top of the base model
    model = Model(inputs=baseModel.input, outputs=headModel)

    return model
    