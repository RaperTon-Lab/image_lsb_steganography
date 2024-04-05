import lsb
import cryptography as cg

if __name__ == "__main__":
    option = input("Choose operation (embed/extract): ").strip().lower()
    if option == "embed":
        cover_image_path = input("Enter the path to the cover image file: ")
        input_image_path = input("Enter the path to the image file to be embedded: ")
        output_image_path = input("Enter the path to save the stego image: ")
        encrypted_data = cg.encrypt_image_menu(input_image_path)
        lsb.embed_data(cover_image_path, encrypted_data, output_image_path)
        print("Operation successfull.")
    elif option == "extract":
        steg_image_path = input("Enter the path to stego image:")
        extracted_bytes = lsb.extract_data(steg_image_path)
        cg.decrypt_image_menu(extracted_bytes)
        print("Extraction successfull.")
    else:
        print("Wrong text")
