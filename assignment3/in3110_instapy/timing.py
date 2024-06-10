from __future__ import annotations

import time
from typing import Callable
from PIL import Image

from . import get_filter, io

from .numpy_filters import numpy_color2gray
from .numba_filters import numba_color2gray


def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    total_time = 0.0
    for _ in range(calls):
        start_time = time.perf_counter()
        filter_function(*arguments)
        end_time = time.perf_counter()
        total_time += end_time - start_time
    return total_time / calls


def make_reports(filename: str = "test/rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """
    # Load the image
    image = io.read_image(filename)
    height, width, _ = image.shape
    print(f"Timing performed using {filename}: {width}x{height}")

    # Define the filter names and implementations
    filter_names = ["color2gray", "color2sepia"]
    implementations = ["numpy", "numba"]

    report_lines = []  # To store lines for the report

    for filter_name in filter_names:
        # Get the reference filter function
        reference_filter = get_filter(filter_name, "python")
        if reference_filter is None:
            continue

        # Time the reference implementation
        reference_time = time_one(reference_filter, image, calls=calls)
        report_lines.append(
            f"Reference (pure Python) filter time {filter_name}: {reference_time:.3f}s ({calls=})"
        )

        # Iterate through the implementations
        for implementation in implementations:
            filter_function = get_filter(filter_name, implementation)
            if filter_function is None:
                continue

            # Time the filter
            filter_time = time_one(filter_function, image, calls=calls)

            # Calculate speedup relative to the reference (pure Python) implementation
            speedup = reference_time / filter_time

            report_lines.append(
                f"Timing: {implementation} {filter_name}: {filter_time:.6f}s (speedup={speedup:.2f}x)"
            )

    # Save the report to a file
    with open("timing-report.txt", "w") as report_file:
        report_file.write(f"Timing performed using {filename}: {width}x{height}\n\n")
        for line in report_lines:
            report_file.write(line + "\n")



if __name__ == "__main__":
    # run as `python -m in3110_instapy.timing`
    make_reports()
