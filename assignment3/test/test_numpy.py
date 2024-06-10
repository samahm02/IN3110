import numpy.testing as nt
import numpy as np
from in3110_instapy.numpy_filters import numpy_color2gray, numpy_color2sepia
from in3110_instapy.python_filters import python_color2gray, python_color2sepia

#Bruker python metodene til å teste ,siden hvis de er like så er shape, data type og pixler like

def test_color2gray(image, reference_gray):
    gray = numpy_color2gray(image)

    assert (reference_gray == gray)


def test_color2sepia(image, reference_sepia):
    sepia = numpy_color2sepia(image)

    nt.assert_allclose(sepia, reference_sepia, rtol=1, atol=0)


if __name__ == "__main__":
    image_path = "rain.jpg"
    test_color2gray(image_path, python_color2gray(image_path))
    test_color2sepia(image_path, python_color2sepia(image_path))
    