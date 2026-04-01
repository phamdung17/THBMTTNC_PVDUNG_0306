import sys
from pathlib import Path

from PIL import Image


END_MARKER = "1111111111111110"


def encode_image(image_path: Path, message: str) -> None:
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    binary_message = "".join(format(ord(char), "08b") for char in message) + END_MARKER
    max_bits = width * height * 3
    if len(binary_message) > max_bits:
        raise ValueError("Thong diep qua dai so voi kich thuoc anh.")

    data_index = 0
    for row in range(height):
        for col in range(width):
            pixel = list(img.getpixel((col, row)))

            for color_channel in range(3):
                if data_index < len(binary_message):
                    pixel[color_channel] = int(
                        format(pixel[color_channel], "08b")[:-1] + binary_message[data_index],
                        2,
                    )
                    data_index += 1

            img.putpixel((col, row), tuple(pixel))

            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    encoded_image_path = image_path.with_name("encoded_image.png")
    img.save(encoded_image_path)
    print("Steganography complete. Encoded image saved as", encoded_image_path.name)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return

    image_path = Path(sys.argv[1])
    message = sys.argv[2]
    encode_image(image_path, message)


if __name__ == "__main__":
    main()
