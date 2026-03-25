from __future__ import annotations

import socket
import threading

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad


HOST = "localhost"
PORT = 12345
BUFFER_SIZE = 4096


def encrypt_message(key: bytes, message: str) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode("utf-8"), AES.block_size))
    return cipher.iv + ciphertext


def decrypt_message(key: bytes, encrypted_message: bytes) -> str:
    iv = encrypted_message[: AES.block_size]
    ciphertext = encrypted_message[AES.block_size :]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode("utf-8")


def create_client_key() -> RSA.RsaKey:
    return RSA.generate(2048)


def decrypt_received_aes_key(client_key: RSA.RsaKey, encrypted_aes_key: bytes) -> bytes:
    cipher_rsa = PKCS1_OAEP.new(client_key)
    return cipher_rsa.decrypt(encrypted_aes_key)


def perform_handshake(client_socket: socket.socket, client_key: RSA.RsaKey) -> bytes:
    server_public_key = RSA.import_key(client_socket.recv(BUFFER_SIZE))
    client_socket.sendall(client_key.publickey().export_key(format="PEM"))
    encrypted_aes_key = client_socket.recv(BUFFER_SIZE)
    return decrypt_received_aes_key(client_key, encrypted_aes_key)


def receive_messages(client_socket: socket.socket, aes_key: bytes) -> None:
    while True:
        encrypted_message = client_socket.recv(BUFFER_SIZE)
        if not encrypted_message:
            break
        print("Received:", decrypt_message(aes_key, encrypted_message))


def start_client(host: str = HOST, port: int = PORT) -> None:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_key = create_client_key()
    aes_key = perform_handshake(client_socket, client_key)

    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket, aes_key),
        daemon=True,
    )
    receive_thread.start()

    try:
        while True:
            message = input("Enter message ('exit' to quit): ")
            client_socket.sendall(encrypt_message(aes_key, message))
            if message == "exit":
                break
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
