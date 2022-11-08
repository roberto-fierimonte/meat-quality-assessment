import os
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns

from loguru import logger

from src.base.utilities import sample_images

IMG_HEIGHT = 720
IMG_WIDTH = 1280
IMG_CHANNELS = ("R", "G", "B")
IMG_LABELS = ("Fresh", "Spoiled")
LABELS_COLOURS = ("green", "red")


def display_images(
    data_path: os.PathLike, seed: int = 456, save_path: Optional[os.PathLike] = None
) -> None:
    """Display a sample of images.

    Args:
        data_path (os.PathLike): Root folder from where to sample the images
        seed (int, optional): Seed for the random number generator used in the sampling.
            Defaults to 456
        save_path (os.PathLike, optional): Folder (not file name) where to save the plots.
            If not provided the plot will not be saved. Defaults to None
    """
    fnames = sample_images(data_path, n_samples=9, seed=seed)
    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(20, 13))
    for e, fn in enumerate(fnames):
        axs.flatten()[e].imshow(mpimg.imread(fn))
        axs.flatten()[e].set_axis_off()

        for lab, col in zip(IMG_LABELS, LABELS_COLOURS):
            if lab in fn:
                axs.flatten()[e].set_title(lab, color=col, fontsize=16)

    fig.suptitle("Samples of the dataset", fontsize=20)
    plt.tight_layout()
    plt.show()

    if save_path is not None:
        fname = os.path.join(save_path, "samples.pdf")
        fig.savefig(fname)
        logger.debug(f"Saved plot to {fname}.")


def display_rgb_images(
    data_path: os.PathLike, seed: int = 456, save_path: Optional[os.PathLike] = None
) -> None:
    """Display a sample of images decomposing them into their RGB components.

    Args:
        data_path (os.PathLike): Root folder from where to sample the images
        dataset_name(str): Name of the dataset being sample (it will appear in the
            title of the plot)
        seed (int, optional): Seed for the random number generator used in the sampling.
            Defaults to 456
        save_path (os.PathLike, optional): Folder (not file name) where to save the plots.
            If not provided the plot will not be saved. Defaults to None
    """
    fnames = sample_images(data_path, n_samples=6, seed=seed)
    fig, axs = plt.subplots(
        nrows=6,
        ncols=6,
        figsize=(28, 16),
        sharex="col",
        sharey="col",
        constrained_layout=True,
    )
    for e, fn in enumerate(fnames):
        sample = mpimg.imread(fn)
        axs[e][0].imshow(sample)
        axs[e][0].set_yticklabels([])
        axs[e][0].set_xticklabels([])
        axs[e][0].set_xticks([])
        axs[e][0].set_yticks([])

        for lab, col in zip(IMG_LABELS, LABELS_COLOURS):
            if lab in fn:
                axs[e][0].set_xlabel(lab, color=col)

        for cid, colour in enumerate(IMG_CHANNELS):
            axs[e][cid + 1].imshow(sample[:, :, cid])
            axs[e][cid + 1].set_xlabel(
                f"Mean {colour} value: {np.mean(sample[:, :, cid]):,.1f}"
            )
            axs[e][cid + 1].set_yticklabels([])
            axs[e][cid + 1].set_xticklabels([])
            axs[e][cid + 1].set_xticks([])
            axs[e][cid + 1].set_yticks([])

            histogram, _ = np.histogram(sample[:, :, cid], bins=256, range=(0, 256))
            sns.histplot(histogram, ax=axs[e][4], color=colour.lower())
            sns.lineplot(histogram, ax=axs[e][5], color=colour.lower())
            axs[e][4].set_xlabel("Pixels in bin")
            axs[e][4].set_ylabel("Number of bins")
            axs[e][5].set_xlabel("Colour value")
            axs[e][5].set_ylabel("Pixels")

    for cid, colour in enumerate(IMG_CHANNELS):
        axs[0][cid + 1].set_title(f"{colour} Channel", fontsize=16)

    axs[0][0].set_title("Original Image", fontsize=16)

    fig.suptitle("Samples of the dataset in RGB", fontsize=20)
    plt.show()

    if save_path is not None:
        fname = os.path.join(save_path, "samples_rgb.pdf")
        fig.savefig(fname)
        logger.debug(f"Saved plot to {fname}.")


def rgb_stats_by_label(
    data_path: os.PathLike, save_path: Optional[os.PathLike] = None
) -> None:
    """Plot aggregated RGB statistics according to the image labels.

    Args:
        data_path (os.PathLike): Root folder from where to read the images
        save_path (os.PathLike, optional): Folder (not file name) where to save the plots.
            If not provided the plot will not be saved. Defaults to None
    """
    fnames = sample_images(data_path, n_samples=-1)

    imgs = dict()
    for lab in IMG_LABELS:
        fnames_lab = [fn for fn in fnames if lab in fn]
        # Pre allocate memory space to read the images, so that we don't have to constantly create
        # new arrays when reading the samples one by one.
        imgs[lab] = np.zeros((len(IMG_CHANNELS), 256), dtype=np.float64)
        for e, fn in enumerate(fnames_lab):
            img = mpimg.imread(fn)
            for cid, colour in enumerate(IMG_CHANNELS):
                imgs[lab][cid, :] += np.histogram(
                    img[:, :, cid], bins=256, range=(0, 256)
                )[0]

    logger.debug("Images loaded")

    fig, axs = plt.subplots(
        nrows=1,
        ncols=len(IMG_LABELS),
        figsize=(20, 6),
        sharey=True,
        constrained_layout=True,
    )

    for cid, colour in enumerate(IMG_CHANNELS):
        for e, lab in enumerate(IMG_LABELS):
            sns.lineplot(imgs[lab][cid], ax=axs[e], color=colour.lower())

            axs[e].set_xlabel("Colour value")
            axs[e].set_ylabel("Pixels")
            axs[e].set_title(f"Label: {lab}")

    fig.suptitle("RGB Statistics of the dataset")
    plt.show()

    if save_path is not None:
        fname = os.path.join(save_path, "stats_rgb.pdf")
        fig.savefig(fname)
        logger.debug(f"Saved plot to {fname}.")
