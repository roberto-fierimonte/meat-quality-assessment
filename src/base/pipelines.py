import os
from typing import Optional, Tuple

import pandas as pd
import tensorflow as tf

from src.base.utilities import sample_images


def images_to_frame(data_path: os.PathLike) -> pd.DataFrame:
    """Read image paths and labels into a DataFrame.

    Search images in a root folder and create a pandas DataFrame where
    each row stored the file path of an image and the corresponding label.

    Args:
        data_path (os.PathLike): Root folder where to search the images. It
            must contain one subfolder per label

    Returns:
        pd.DataFrame: DataFrame that contains the list of images and their
            corresponding labels
    """
    fnames = sample_images(data_path, n_samples=-1)
    res = pd.DataFrame(
        {"image_path": fnames, "label": [f.split("/")[-2] for f in fnames]}
    )
    res["target"] = [1 if x == "Fresh" else 0 for x in res["label"]]
    return res


def decode_image(
    filename: os.PathLike,
    label: int,
    image_size: Tuple[int, int] = (32, 32),
    n_labels: Optional[int] = None,
) -> Tuple[tf.Tensor, Optional[tf.Tensor]]:
    """Reads, decode, and return an image as a Tensorflow tensor.

    Args:
        filename (os.PathLike): File name of the image
        label (int): Numerical label of the image
        image_size (Tuple[int, int], optional): Dimension of the imagine in (width, height) pixels.
            Default to (32, 32)
        n_labels (int, optional): Number of different labels in the entire dataset. Must be provided
            if `label` is not None. Default to None

    Returns:
        tf.Tensor: Tensor representation of the image
        Optional[tf.Tensor]: If the label is present, tensor representation of the label
    """
    bits = tf.io.read_file(filename)
    image = tf.image.decode_jpeg(bits, channels=3)
    image = tf.cast(image, tf.float32)
    image /= 255.0
    image = tf.image.resize(image, image_size)

    if label is None:
        return image
    else:
        return image, tf.one_hot(label, depth=n_labels)


def augment_image(
    image: tf.Tensor, label: Optional[tf.Tensor] = None
) -> Tuple[tf.Tensor, Optional[tf.Tensor]]:
    """Apply augmentation techniques to an image in order to reduce overfitting in the model.

    Args:
        image (tf.Tensor): Tensor representation of an image
        label (tf.Tensor): Tensor representation of the label

    Returns:
        tf.Tensor: Tensor representation of the augmented image
        Optional[tf.Tensor]: If the label is present, tensor representation of the label
    """
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_flip_up_down(image)
    image = tf.image.random_brightness(image, 0.2)
    image = tf.image.random_contrast(image, lower=0.3, upper=0.9)

    if label is None:
        return image
    else:
        return image, label
