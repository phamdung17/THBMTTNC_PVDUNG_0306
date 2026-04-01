import socket
import ssl
import threading
from pathlib import Path


SERVER_ADDRESS = ("localhost", 12345)
BASE_DIR = Path(__file__).resolve().parent
CERT_DIR = BASE_DIR / "certificates"
CERT_FILE = CERT_DIR / "server-cert.crt"
KEY_FILE = CERT_DIR / "server-key.key"
clients: list[ssl.SSLSocket] = []
clients_lock = threading.Lock()


def remove_client(client_socket: ssl.SSLSocket) -> None:
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)


def broadcast_message(sender_socket: ssl.SSLSocket, data: bytes) -> None:
    with clients_lock:
        other_clients = [client for client in clients if client != sender_socket]

    for client in other_clients:
        try:
            client.sendall(data)
        except OSError:
            remove_client(client)


def handle_client(client_socket: ssl.SSLSocket) -> None:
    with clients_lock:
        clients.append(client_socket)

    print("Da ket noi voi:", client_socket.getpeername())

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            print("Nhan:", data.decode("utf-8"))
            broadcast_message(client_socket, data)
    except OSError as exc:
        print("Loi ket noi client:", exc)
    finally:
        print("Da ngat ket noi:", client_socket.getpeername())
        remove_client(client_socket)
        client_socket.close()


def create_ssl_context() -> ssl.SSLContext:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    return context


def main() -> None:
    if not CERT_FILE.exists() or not KEY_FILE.exists():
        raise FileNotFoundError(
            "Chua tim thay chung chi SSL. Hay chay make-cert.bat hoac tao file server-cert.crt/server-key.key."
        )

    context = create_ssl_context()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(5)

    print("Server dang cho ket noi tai", f"{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}")

    while True:
        client_socket, _ = server_socket.accept()
        ssl_socket = context.wrap_socket(client_socket, server_side=True)
        client_thread = threading.Thread(target=handle_client, args=(ssl_socket,), daemon=True)
        client_thread.start()


if __name__ == "__main__":
    main()
