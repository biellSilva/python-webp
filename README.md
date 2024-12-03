# PyWebp: Image to WebP Converter

Pywebp is a versatile command-line tool written in Python for converting images to the WebP format. WebP offers superior lossless and lossy compression, enabling smaller, richer images that enhance web performance.

## Key Features

- **Ease of Use**: Convert single images or entire directories with simple commands.
- **Versatility**: Options for recursive processing and maintaining directory structure.
- **Quality Control**: Adjust output quality, optimize, and resize images.
- **Advanced Features**:
  - Multithreading for faster processing of large batches.
  - Verbose output for detailed feedback or quiet mode for minimal output.
  - Unlink input images after processing to manage disk space.

Whether you're a web developer optimizing site images or a photographer converting your portfolio, Pywebp provides a comprehensive solution for your image conversion needs.

## Arguments

### Positional Parameters

- `input`: Input directory. Default is the current directory.
- `output`: Output directory. Default is the current directory.

### Options

- `resize`: Resize image to the given size. e.g., 640x800.
- `min-width`: Skips images that are smaller than the given width.
- `min-height`: Skips images that are smaller than the given height.
- `max-width`: Skips images that are larger than the given width.
- `max-height`: Skips images that are larger than the given height.
- `keep-aspect-ratio`: Keep the original aspect ratio while resizing. Default is True.
- `files-format`: Input files format. e.g., png, jpg, jpeg.
- `quality`: Integer, 0-100. For lossy, 0 gives the smallest size and 100 the largest. For lossless, this parameter is the amount of effort put into the compression: 0 is the fastest, but gives larger files compared to the slowest, but best, 100. Default is 80.
- `alpha-quality`: Integer, 0-100. For lossy compression only. 0 gives the smallest size and 100 is lossless. Default is 100.
- `lossless`: Enable lossless compression. Default is False.
- `method`: Quality/speed trade-off (0=fast, 6=slower-better). Default is 4.
- `exact`: If true, preserve the transparent RGB values. Otherwise, discard invisible RGB values for better compression. Default is False.
- `keep-directory`: Keep the directory structure of the input. Default is True.
- `recursive`: Convert images in subdirectories. Default is False.
- `use-threads`: Use multiple threads. Default is False.
- `threads`: Number of threads to use. None = Max possible (4 * N of cores, limited to 32).
- `unlink`: Unlink/delete the input files. Default is False.
- `ignore-existing`: Ignore existing files. Default is True.

## Usage

To convert images using Pywebp, you can use the following command:

```sh
pywebp convert ./input_directory ./output_directory --resize 640x800 --quality 90 --lossless --recursive
```

This command will:

- Convert all images in the ./images directory to WebP format.
- Resize the images to 640x800 pixels.
- Set the quality of the output images to 90.
- Enable lossless compression.
- Process images in subdirectories of the ./images directory.

You can adjust the parameters as needed to fit your specific use case.
