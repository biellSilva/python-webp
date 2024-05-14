# Pywebp: Image to WebP Converter

Pywebp is a powerful, flexible command-line tool written in Python that allows you to convert images into the WebP format. WebP is a modern image format that provides superior lossless and lossy compression for images on the web. Using WebP, webmasters and web developers can create smaller, richer images that make the web faster.

The tool is designed to be easy to use, yet versatile. It can handle single image files as well as entire directories, with options for recursive processing and maintaining the original directory structure. It also provides control over the quality of the output images, with options for optimization and resizing.

In addition to its core functionality, Pywebp offers a range of advanced features. It supports multithreading for faster processing of large batches of images. It also provides options for verbose output for detailed feedback during processing, or quiet mode for minimal output.

One of the unique features of Pywebp is its ability to unlink the input image after processing, which can be useful for managing disk space during large batch conversions.

Whether you're a web developer looking to optimize your site's images, or a photographer looking to convert your portfolio to a more efficient format, Pywebp provides a comprehensive solution for your image conversion needs.

## Arguments

Here is a detailed list of the command-line arguments that Pywebp accepts:

- `input`: This is the path to the input image file or directory. This argument is required. Pywebp will convert all image files in the specified directory and its subdirectories.

- `-o` or `--output`: This is the path to the output directory where the converted images will be saved. By default, it is set to `./output`. The output images will have the same directory structure as the input.

- `-q` or `--quality`: This is the quality of the output image. It accepts an integer value between 0 and 100, where 0 is the lowest quality and 100 is the highest. By default, it is set to `80`.

- `-opt` or `--optimizer`: This flag indicates whether to use optimization when saving the image. It doesn't require a value. If this flag is present, the image will be optimized, which can result in a smaller file size without significant loss in image quality.

- `-s` or `--size`: This is used to resize the image to the specified size. The size should be specified as `widthxheight` (e.g., `640x480`). If this argument is not provided, the image will keep its original size.

- `-nr` or `--no-recursive`: This flag indicates whether to process directories recursively. If this flag is present, only the images in the specified directory will be processed, and the images in its subdirectories will be ignored.

- `-kd` or `--keep-directory`: This flag indicates whether to keep the directory structure of the input images in the output directory. If this flag is present, the output images will have the same directory structure as the input images.

- `-u` or `--unlink`: This flag indicates whether to unlink the input image after processing. If this flag is present, the input image will be deleted after it is converted.

- `-v` or `--verbose`: This flag indicates whether to print verbose output. If this flag is present, Pywebp will print detailed output about the conversion process.

- `-qt` or `--quiet`: This flag indicates whether to print no output. If this flag is present, Pywebp will not print any output.

- `-t` or `--threads`: This is the number of threads to use for processing. It accepts an integer value. If this argument is not provided, Pywebp will use a default number of threads.

- `-nt` or `--no-threads`: This flag indicates whether not to use threads for processing. If this flag is present, Pywebp will process the images sequentially.

## Usage

You can use Pywebp by running the following command in your terminal:

```bash
pywebp input [-o output] [-q quality] [-opt] [-s size] [-nr] [-kd] [-u] [-v] [-qt] [-t threads] [-nt]
```

Replace `input` with the path to your input image file or directory. The rest of the arguments are optional. If you don't provide an optional argument, its default value will be used.
