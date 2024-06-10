"""numpy implementation of image filters"""
from __future__ import annotations

import numpy as np


def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    # henter ut RGB channels fra input
    red_channel = image[:, :, 0]
    green_channel = image[:, :, 1]
    blue_channel = image[:, :, 2]

    # gjør om til grayscale
    gray_image = 0.21 * red_channel + 0.72 * green_channel + 0.07 * blue_channel

    # gjør om til riktig datatype
    gray_image = gray_image.astype(np.uint8)

    return gray_image


def numpy_color2sepia(image: np.array, k: float = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
        you may ignore it)

    Returns:
        np.array: sepia_image
    """
    if not 0 <= k <= 1:
        raise ValueError(f"k must be between [0-1], got {k=}")

    sepia_image = np.empty_like(image)
 
    sepia_matrix = np.array([
        [ 1 - ((1 - 0.393) * k), 0.769 * k, 0.189 * k],
        [ 0.349 * k, 1 - ((1 - 0.686) * k), 0.168 * k],
        [ 0.272 * k, 0.534 * k, 1 - ((1 - 0.131) * k)],
    ])

    sepia_image = np.einsum('ijk,lk->ijl', image, sepia_matrix)
    sepia_image[sepia_image > 255] = 255

    sepia_image = sepia_image.astype("uint8")
    return sepia_image
