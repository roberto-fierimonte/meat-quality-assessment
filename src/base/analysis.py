import os
import glob
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns


def _sample_images(
    data_path: os.PathLike, n_samples: int, seed: Optional[int] = None
) -> list:
    """Sample a number of images from a root folder and its subfolders.

    Args:
        data_path (os.PathLike): Root folder from where to sample the images
        n_samples (int): Number of images to sample. Must be greater than or equal to 1
        seed (int, optional): Seed for the random number generator used in the sampling.
            Defaults to None

    Raises:
        ValueError: If any of the input parameters is incorrect

    Returns:
        list: list of paths of the sampled images
    """
    try:
        assert n_samples >= 1
    except AssertionError:
        msg = "The number of samples must be greater than or equal to 1."
        raise ValueError(msg)

    if not data_path.endswith("/"):
        data_path += "/"
    rng = np.random.default_rng(seed=seed)
    samples = rng.choice(
        [
            os.path.join(data_path, f)
            for f in glob.iglob(data_path + "**/*.jpg", recursive=True)
        ],
        size=n_samples,
        replace=False,
    )
    return samples


def display_images(data_path: os.PathLike, dataset_name: str, seed: int = 456) -> None:
    """Display a sample of images.

    Args:
        data_path (os.PathLike): Root folder from where to sample the images
        dataset_name(str): Name of the dataset being sample (it will appear in the
            title of the plot)
        seed (int, optional): Seed for the random number generator used in the sampling.
            Defaults to 456
    """
    samples = _sample_images(data_path, n_samples=9, seed=seed)
    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(20, 13))
    for e, s in enumerate(samples):
        axs.flatten()[e].imshow(mpimg.imread(s))
        axs.flatten()[e].set_axis_off()

        if "Fresh" in s:
            axs.flatten()[e].set_title("Fresh", color="green", fontsize=16)
        elif "Spoiled" in s:
            axs.flatten()[e].set_title("Spoiled", color="red", fontsize=16)

    fig.suptitle(f"Samples of {dataset_name}", fontsize=20)
    plt.tight_layout()
    plt.show()


def display_rgb_images(
    data_path: os.PathLike, dataset_name: str, seed: int = 456
) -> None:
    """Display a sample of images decomposing them into their RGB components.

    Args:
        data_path (os.PathLike): Root folder from where to sample the images
        dataset_name(str): Name of the dataset being sample (it will appear in the
            title of the plot)
        seed (int, optional): Seed for the random number generator used in the sampling.
            Defaults to 456
    """
    samples = _sample_images(data_path, n_samples=6, seed=seed)
    colors = ("r", "g", "b")
    fig, axs = plt.subplots(nrows=6, ncols=6, figsize=(28, 16), constrained_layout=True)
    for e, s in enumerate(samples):
        sample = mpimg.imread(s)
        axs[e][0].imshow(sample)
        axs[e][0].set_yticklabels([])
        axs[e][0].set_xticklabels([])
        axs[e][0].set_xticks([])
        axs[e][0].set_yticks([])

        if "Fresh" in s:
            axs[e][0].set_xlabel("Fresh", color="green")
        elif "Spoiled" in s:
            axs[e][0].set_xlabel("Spoiled", color="red")

        for cid, colour in enumerate(colors):
            axs[e][cid + 1].imshow(sample[:, :, cid])
            axs[e][cid + 1].set_xlabel(
                f"Mean {colour.upper()} value: {np.mean(sample[:, :, cid]):,.1f}"
            )
            axs[e][cid + 1].set_yticklabels([])
            axs[e][cid + 1].set_xticklabels([])
            axs[e][cid + 1].set_xticks([])
            axs[e][cid + 1].set_yticks([])

            histogram, _ = np.histogram(sample[:, :, cid], bins=256, range=(0, 256))
            sns.histplot(histogram, ax=axs[e][4], color=colour)
            sns.lineplot(histogram, ax=axs[e][5], color=colour)
            axs[e][4].set_xlabel("Pixels in bin")
            axs[e][4].set_ylabel("Number of bins")
            axs[e][5].set_xlabel("Colour value")
            axs[e][5].set_ylabel("Pixels")

    axs[0][0].set_title("Original Image", fontsize=16)
    axs[0][1].set_title("R Channel", fontsize=16)
    axs[0][2].set_title("G Channel", fontsize=16)
    axs[0][3].set_title("B Channel", fontsize=16)

    fig.suptitle(f"Samples of {dataset_name} in RGB", fontsize=20)
    # plt.tight_layout(pad=0.3)
    # plt.subplots_adjust()
    plt.show()
