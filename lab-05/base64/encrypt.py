import base64
from pathlib import Path


DATA_FILE = Path(__file__).with_name("data.txt")


def main() -> None:
    input_string = input("Nhap thong tin can ma hoa: ")

    encoded_bytes = base64.b64encode(input_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")

    DATA_FILE.write_text(encoded_string, encoding="utf-8")
    print(f"Da ma hoa va ghi vao tep {DATA_FILE.name}")


if __name__ == "__main__":
    main()
