from argparse import ArgumentParser


def get_argparser():
    parser = ArgumentParser(description="Convert images to WebP format")

    parser.add_argument("input", help="Input image file or directory")
    parser.add_argument(
        "-o",
        "--output",
        help="Output image file or directory",
        default="./output",
        dest="output",
    )

    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=80,
        help="Quality of the output image",
        dest="quality",
    )
    parser.add_argument(
        "-opt",
        "--optimizer",
        action="store_true",
        help="Use optimization when saving the image",
        dest="optimize",
    )
    parser.add_argument(
        "-s",
        "--size",
        help="Resize the image to the specified size (e.g. 640x480)",
        dest="size",
    )
    parser.add_argument(
        "-nr",
        "--no-recursive",
        action="store_false",
        help="Process directories recursively",
        dest="recursive",
    )
    parser.add_argument(
        "-kd",
        "--keep-directory",
        action="store_true",
        help="Keep the directory structure of the input images",
    )

    parser.add_argument(
        "-u",
        "--unlink",
        action="store_true",
        help="Unlink the input image after processing",
    )

    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose output",
        dest="verbose",
    )
    verbosity_group.add_argument(
        "-qt",
        "--quiet",
        action="store_false",
        help="Print no output",
        dest="verbose",
    )

    thread_group = parser.add_mutually_exclusive_group()
    thread_group.add_argument(
        "-t",
        "--threads",
        type=int,
        help="Number of threads to use for processing",
        dest="threads",
    )
    thread_group.add_argument(
        "-nt",
        "--no-threads",
        action="store_true",
        help="Won't use threads for processing",
        dest="no_threads",
    )

    return parser.parse_args()
