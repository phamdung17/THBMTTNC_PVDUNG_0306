from __future__ import annotations

import socket
import threading
from typing import List, Tuple

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


HOST = "localhost"
PORT = 12345
BUFFER_SIZE = 4096


ClientEntry = Tuple[socket.socket, bytes]


server_key = RSA.generate(2048)
clients: List[ClientEntry] = []
clients_lock = threading.Lock()


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


def export_public_key() -> bytes:
    return server_key.publickey().export_key(format="PEM")


def decrypt_aes_key(encrypted_aes_key: bytes) -> bytes:
    cipher_rsa = PKCS1_OAEP.new(server_key)
    return cipher_rsa.decrypt(encrypted_aes_key)


def build_encrypted_aes_key(client_public_key_pem: bytes) -> tuple[bytes, bytes]:
    client_received_key = RSA.import_key(client_public_key_pem)
    aes_key = get_random_bytes(16)
    cipher_rsa = PKCS1_OAEP.new(client_received_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    return aes_key, encrypted_aes_key


def broadcast_message(sender_socket: socket.socket, message: str) -> None:
    with clients_lock:
        recipients = list(clients)

    for client_socket, client_key in recipients:
        if client_socket is sender_socket:
            continue
        client_socket.sendall(encrypt_message(client_key, message))


def handle_client(client_socket: socket.socket, client_address) -> None:
    print(f"Connected with {client_address}")
    aes_key = b""

    try:
        client_socket.sendall(export_public_key())
        client_public_key_pem = client_socket.recv(BUFFER_SIZE)
        aes_key, encrypted_aes_key = build_encrypted_aes_key(client_public_key_pem)
        client_socket.sendall(encrypted_aes_key)

        with clients_lock:
            clients.append((client_socket, aes_key))

        while True:
            encrypted_message = client_socket.recv(BUFFER_SIZE)
            if not encrypted_message:
                break

            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print(f"Received from {client_address}: {decrypted_message}")

            if decrypted_message == "exit":
                break

            broadcast_message(client_socket, decrypted_message)
    finally:
        with clients_lock:
            if aes_key and (client_socket, aes_key) in clients:
                clients.remove((client_socket, aes_key))
        client_socket.close()
        print(f"Connection with {client_address} closed")


def create_server_socket(host: str = HOST, port: int = PORT) -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    return server_socket


def start_server(host: str = HOST, port: int = PORT) -> None:
    server_socket = create_server_socket(host, port)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address),
            daemon=True,
        )
        thread.start()


if __name__ == "__main__":
    start_server()
