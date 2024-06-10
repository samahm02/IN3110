"""numba-optimized filters"""
from __future__ import annotations

import numpy as np
from numba import jit

@jit(nopython=True)
def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    height, width, _ = image.shape


    gray_image = np.empty((height, width), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            red, green, blue = image[i, j]
            gray_value = int(0.21 * red + 0.72 * green + 0.07 * blue)
            gray_image[i, j] = gray_value

    return gray_image


def numba_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    shape =  np.asarray((np.shape(image)))

    sepia_matrix = [
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131],
]
    for y in range(shape[0]):
        for x in range(shape[1]):
            r, g, b = image[y, x]
           
            red_channel = int(r * sepia_matrix[0][0] + g * sepia_matrix[0][1] + b * sepia_matrix[0][2])
            green_channel = int(r * sepia_matrix[1][0] + g * sepia_matrix[1][1] + b * sepia_matrix[1][2])
            blue_channel = int(r * sepia_matrix[2][0] + g * sepia_matrix[2][1] + b * sepia_matrix[2][2])
           
            sepia_image[y, x] = (
                min(255, red_channel),
                min(255, green_channel),
                min(255, blue_channel)
            )

    sepia_image = sepia_image.astype('uint8')
    return sepia_image



