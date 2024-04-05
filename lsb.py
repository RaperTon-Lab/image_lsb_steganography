from PIL import Image


def get_number_of_pixels(image_path):
    """
    Get the total number of pixels in an image.

    :param image_path: The path to the image file.
    :return: The total number of pixels in the image.
    """
    input_image = Image.open(image_path)
    width, height = input_image.size
    return width * height


def suggest_image_size(encrypted_bits):
    """
    Suggest a suitable image size to embed the encrypted file.

    :param encrypted_file_path: The path to the encrypted file.
    :return: A tuple representing the suggested image size (width, height).
    """
    encrypted_bits_count = len(encrypted_bits) * 8

    # Calculate the number of pixels needed to embed the encrypted file
    total_pixels_needed = (
        encrypted_bits_count + 64
    )  # Additional 64 pixels for storing the size
    suggested_width = int(total_pixels_needed**0.5)
    suggested_height = int(total_pixels_needed / suggested_width)

    return (suggested_width, suggested_height)


def resize_image(input_image_path, output_image_path, size):
    """
    Resize an image.

    :param input_image_path: The path to the input image file.
    :param output_image_path: The path to save the resized image.
    :param size: A tuple (width, height) representing the desired size of the output image.
    """
    input_image = Image.open(input_image_path)
    resized_image = input_image.resize(size)
    resized_image.save(output_image_path)


def embed_data(input_image_path, encrypted_bits, output_image_path):
    """
    Embed data into an image.

    :param input_image_path: The path to the input image file.
    :param encrypted_file_path: The path to the encrypted file.
    :param output_image_path: The path to save the modified image.
    """
    # Check if resizing is needed
    image_pixels = get_number_of_pixels(input_image_path)
    encrypted_bits_count = len(encrypted_bits) * 8
    total_pixels_needed = encrypted_bits_count + 64
    encrypted_bits_binary = bin(int.from_bytes(encrypted_bits, byteorder="big"))[2:]

    encrypted_bits_count_binary = bin(encrypted_bits_count)[2:].zfill(64)
    print(f"Encrypted length {encrypted_bits_count}")
    print(f"Binary  {encrypted_bits_count_binary}")
    if image_pixels < total_pixels_needed:
        print("Resizing image...")
        suggested_size = suggest_image_size(encrypted_bits)
        resize_image(input_image_path, input_image_path, suggested_size)

    # Open the input image
    input_image = Image.open(input_image_path)
    width, height = input_image.size

    # Open the encrypted file and read its bits
    final_encrypted_bits = encrypted_bits_count_binary + encrypted_bits_binary

    # Embed the size of the encrypted file (64-bit binary) into the first 64 pixels
    # input_image = Image.new(input_image.mode, (width, height))

    # Iterator for the encrypted bits
    encrypted_bits_iter = iter(final_encrypted_bits)

    # Iterate over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the pixel value at the current position
            pixel = list(input_image.getpixel((x, y)))

            # Modify the least significant bit (LSB) of each color channel (R, G, B)
            for i in range(3):  # 3 color channels: R, G, B
                # Get the next bit from the encrypted file
                try:
                    bit = next(encrypted_bits_iter)
                except StopIteration:
                    # If all bits from the encrypted file are used, stop modifying the image
                    input_image.save(output_image_path)
                    return

                # Modify the LSB of the current color channel
                pixel[i] = (pixel[i] & ~1) | int(bit)

            # Set the modified pixel value in the new image
            input_image.putpixel((x, y), tuple(pixel))

    # Save the modified image
    input_image.save(output_image_path)
    print("Image saved successfully.")


def extract_data(input_image_path):
    """
    Extract embedded data from an image.

    :param input_image_path: The path to the input image file.
    :param output_file_path: The path to save the extracted data.
    """
    # Open the input image
    modified_image = Image.open(input_image_path)
    width, height = modified_image.size

    first_64_bits = ""
    extracted_bits = ""
    length = 0
    j = 1
    # Iterate over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the pixel value at the current position
            pixel = modified_image.getpixel((x, y))

            # Extract the least significant bit (LSB) of each color channel (R, G, B)
            for i in range(3):  # 3 color channels: R, G, B
                if j < 65:
                    first_64_bits += str(pixel[i] & 1)
                    first_64_bits
                    length = int(first_64_bits, 2)
                    j += 1
                    # print(f"value of {j}")
                else:
                    extracted_bits += str(pixel[i] & 1)
                    length -= 1
                    # print(f"value of len{length}")
                    if length <= 0:
                        print("Extraction of bits completed.")
                        print(len(extracted_bits))
                        extracted_bytes = bytes(
                            int(extracted_bits[i : i + 8], 2)
                            for i in range(0, len(extracted_bits), 8)
                        )
                        return extracted_bytes


if __name__ == "__main__":
    operation_choice = input("Choose operation (embed/extract): ").strip().lower()

    if operation_choice == "embed":
        input_image_path = input("Enter the path to the cover image file: ")
        encrypted_file_path = input("Enter the path to the encrypted file: ")
        output_image_path = input("Enter the path to save the stego image: ")

        embed_data(input_image_path, encrypted_file_path, output_image_path)

    elif operation_choice == "extract":
        input_image_path = input("Enter the path to the stego image file: ")
        output_file_path = input("Enter the path to save the extracted file: ")

        extract_data(input_image_path, output_file_path)

    else:
        print("Invalid operation choice. Please choose 'embed' or 'extract'.")
