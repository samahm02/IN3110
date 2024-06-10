"""Command-line (script) interface to instapy"""
from __future__ import annotations

import argparse
import sys

import in3110_instapy as ins
import numpy as np
from PIL import Image

from . import io


def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
) -> None:
    """Run the selected filter"""
    # load the image from a file
    image = Image.open(file)
    if scale != 1:
        # Resize image, if needed
        image = image.resize((image.width // int(scale), image.height // int(scale)))


    # Apply the filter
    image = np.asarray(image)
    filter = ins.get_filter(filter, implementation)
    filtered = filter(image)

    if out_file:
        io.write_image(filtered, out_file)
        # save the file
    else:
        # not asked to save, display it instead
        io.display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")
    parser.add_argument("-o", "--out", help="The output filename")
    # Add required arguments
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-g", "--gray", help="Select gray filter", action="store_true")
    group.add_argument("-se", "--sepia", help="Select sepia filter", action="store_true")
    parser.add_argument("-sc", "--scale", help="Scale factor to resize image")
    parser.add_argument("-i ", "--implementation", help="The implementation", choices={"python", "numpy", "numba"})

    # parse arguments and call run_filter
    args = parser.parse_args()
    
    if not args.scale:
        args.scale = 1

    if not args.implementation:
        args.implementation = "python"

    if args.sepia: 
        args.filter = "color2sepia"
    else:
        args.filter = "color2gray"
        
    run_filter(args.file, args.implementation, args.filter, args.scale, args.out)


