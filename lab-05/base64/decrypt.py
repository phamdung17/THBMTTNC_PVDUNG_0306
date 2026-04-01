import base64
from pathlib import Path


DATA_FILE = Path(__file__).with_name("data.txt")


def main() -> None:
    try:
        encoded_string = DATA_FILE.read_text(encoding="utf-8").strip()
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode("utf-8")
        print("Chuoi sau khi giai ma:", decoded_string)
    except Exception as exc:
        print("Loi:", exc)


if __name__ == "__main__":
    main()
