import os
import glob
from typing import Optional

import numpy as np


def sample_images(
    data_path: os.PathLike, n_samples: int, seed: Optional[int] = None
) -> np.array:
    """Sample a number of images from a root folder and its subfolders.

    Args:
        data_path (os.PathLike): Root folder from where to sample the images
        n_samples (int): Number of images to sample. Must be equal to -1 (all images are
            sampled), or greater than or equal to 1
        seed (int, optional): Seed for the random number generator used in the sampling.
            Not used if `n_samples` = -1. Defaults to None

    Raises:
        ValueError: If any of the input parameters is incorrect

    Returns:
        np.array: array of paths of the sampled images
    """
    try:
        assert (n_samples == -1 or n_samples >= 1)
    except AssertionError:
        msg = "The number of samples must be equal to -1, or greater than or equal to 1."
        raise ValueError(msg)

    if not data_path.endswith("/"):
        data_path += "/"

    fnames = [f for f in glob.iglob(data_path + "**/*.jpg", recursive=True)]

    if n_samples >= 1:
        rng = np.random.default_rng(seed=seed)
        samples = rng.choice(fnames, size=n_samples, replace=False)
        return samples
    else:
        return np.array(fnames)
