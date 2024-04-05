from PIL import Image


def print_image_info(image_path):
    """
    Print basic information about an image.

    :param image_path: The path to the image file.
    """
    try:
        # Open the image
        image = Image.open(image_path)

        # Print image format, size, mode, and color depth
        print("Image Format:", image.format)
        print("Image Size:", image.size)
        print("Image Mode:", image.mode)
        print("Image Color Depth:", image.bits)
    except Exception as e:
        print("Error:", e)


def resize_image(input_image_path, output_image_path, size):
    """
    Resize an image.

    :param input_image_path: The path to the input image file.
    :param output_image_path: The path to save the resized image.
    :param size: A tuple (width, height) representing the desired size of the output image.
    """
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)


if __name__ == "__main__":
    input_image_path = input("Enter the path to the input image file: ")
    output_image_path = input("Enter the path to save the resized image: ")
    width = int(input("Enter the width of the resized image: "))
    height = int(input("Enter the height of the resized image: "))
    size = (width, height)

    resize_image(input_image_path, output_image_path, size)
    print("Image resized and saved successfully!")
