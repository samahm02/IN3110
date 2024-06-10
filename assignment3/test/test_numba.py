import numpy.testing as nt
from in3110_instapy.numba_filters import numba_color2gray, numba_color2sepia
from in3110_instapy.python_filters import python_color2gray, python_color2sepia

#Bruker python metodene til å teste ,siden hvis de er like så er shape, data type og pixler like

def test_color2gray(image, reference_gray):
    gray = numba_color2gray(image)

    assert (reference_gray == gray)


def test_color2sepia(image, reference_sepia):
    sepia = numba_color2sepia(image)

    assert (reference_sepia == sepia)




if __name__ == "__main__":
    image_path = "rain.jpg"
    test_color2gray(image_path, python_color2gray(image_path))
    
    test_color2sepia(image_path, python_color2sepia(image_path))