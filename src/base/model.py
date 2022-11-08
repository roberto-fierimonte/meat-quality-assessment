import tensorflow as tf
from tensorflow.keras import layers


class CNNModel(tf.keras.Model):
    """Simple CNN model."""

    def __init__(self, width: int, height: int, *args, **kwargs):
        """Initialise all the layers in the model.

        Args:
            width (int): Width of the input image
            height (int): Height of the input image
        """
        super().__init__(*args, **kwargs)

        self.conv2d_1 = layers.Conv2D(
            35, (3, 3), activation="relu", input_shape=(width, height, 3)
        )
        self.maxpool2d_1 = layers.MaxPooling2D((2, 2))
        self.conv2d_2 = layers.Conv2D(64, (3, 3), activation="relu")
        self.maxpool2d_2 = layers.MaxPooling2D((2, 2))
        self.conv2d_3 = layers.Conv2D(64, (3, 3), activation="relu")

        self.flatten = layers.Flatten()
        self.dense1 = layers.Dense(64, activation="relu")
        self.dense2 = layers.Dense(2)

    def call(self, inputs: tf.Tensor) -> tf.Tensor:
        """Call the model on some inputs and return the output.

        Args:
            inputs (tf.Tensor): Inputs to the model

        Returns:
            tf.Tensor: Output of the model given the inputs
        """
        x = self.conv2d_1(inputs)
        x = self.maxpool2d_1(x)
        x = self.conv2d_2(x)
        x = self.maxpool2d_2(x)
        x = self.conv2d_3(x)
        x = self.flatten(x)
        x = self.dense1(x)
        x = self.dense2(x)
        return x
