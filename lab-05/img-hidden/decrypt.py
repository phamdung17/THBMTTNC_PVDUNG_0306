import sys
from pathlib import Path

from PIL import Image


END_MARKER = "1111111111111110"


def decode_image(encoded_image_path: Path) -> str:
    img = Image.open(encoded_image_path).convert("RGB")
    width, height = img.size
    binary_message = ""

    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            for color_channel in range(3):
                binary_message += format(pixel[color_channel], "08b")[-1]

    end_index = binary_message.find(END_MARKER)
    if end_index == -1:
        return ""

    binary_message = binary_message[:end_index]
    chars = [
        chr(int(binary_message[i : i + 8], 2))
        for i in range(0, len(binary_message), 8)
        if len(binary_message[i : i + 8]) == 8
    ]
    return "".join(chars)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return

    encoded_image_path = Path(sys.argv[1])
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)


if __name__ == "__main__":
    main()
