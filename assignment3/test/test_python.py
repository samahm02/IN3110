from in3110_instapy.python_filters import python_color2gray, python_color2sepia

import numpy as np
from PIL import Image
import numpy.testing as npt

import random as rn

def test_color2gray(image_path):
    image = Image.open(image_path)

    # gjør om til  numpy array
    pixel = np.asarray(image)

    # henter svar fra python_color2gray
    grayPy = python_color2gray(pixel)

    # tester 3 pixler
    width = grayPy.shape[0]
    height = grayPy.shape[1]
    test_array = np.ones(3)
    for n in range(3):
        i = rn.randint(0, width-1)
        j = rn.randint(0, height-1)
        r, g, b = grayPy[i][j]
        test_array[n] = r == g == b

    assert (type(grayPy[1][1][0]) == np.uint8)  # sjekker data type
    assert (pixel.shape == grayPy.shape)  # sjekker shape
    assert (all(test_array))  # sjekker rgb verdiene





def test_color2sepia(image_path):
    image = Image.open(image_path)
    pixel = np.asarray(image)

    sepiaPy = python_color2sepia(pixel)

    width = sepiaPy.shape[0]
    height = sepiaPy.shape[1]
    assert (type(sepiaPy[1][1][0]) == np.uint8)  # sjekker data type
    assert (pixel.shape == sepiaPy.shape)  # sjekker shape

    
    sepia_matrix = [
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131],
    ]

    # setter toleranse for np.allclose
    tolerance = 1.0

    for _ in range(3):
        i = rn.randint(0, width-1)
        j = rn.randint(0, height-1)
        r, g, b = pixel[i][j]
        r_s, g_s, b_s = sepiaPy[i][j]

        expected_r_s = np.clip(r * sepia_matrix[0][0] + g * sepia_matrix[0][1] + b * sepia_matrix[0][2], 0, 255)
        expected_g_s = np.clip(r * sepia_matrix[1][0] + g * sepia_matrix[1][1] + b * sepia_matrix[1][2], 0, 255)
        expected_b_s = np.clip(r * sepia_matrix[2][0] + g * sepia_matrix[2][1] + b * sepia_matrix[2][2], 0, 255)
        
        if not np.allclose([r_s, g_s, b_s], [expected_r_s, expected_g_s, expected_b_s], rtol=tolerance, atol=tolerance):
            print(f"Assertion error at pixel ({i}, {j}):")
            print(f"Actual: R={r_s}, G={g_s}, B={b_s}")
            print(f"Expected: R={expected_r_s}, G={expected_g_s}, B={expected_b_s}")

        assert np.allclose([r_s, g_s, b_s], [expected_r_s, expected_g_s, expected_b_s], rtol=tolerance, atol=tolerance)




if __name__ == "__main__":
    image_path = "rain.jpg"
    test_color2gray(image_path)
    test_color2sepia(image_path)
