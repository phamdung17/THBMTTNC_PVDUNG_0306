from __future__ import annotations

import random

import tornado.ioloop
import tornado.web
import tornado.websocket


class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self) -> None:
        WebSocketServer.clients.add(self)

    def on_close(self) -> None:
        WebSocketServer.clients.remove(self)

    @classmethod
    def send_message(cls, message: str) -> None:
        print(f"Sending message {message} to {len(cls.clients)} client(s).")
        for client in list(cls.clients):
            client.write_message(message)


class RandomWordSelector:
    def __init__(self, word_list):
        self.word_list = word_list

    def sample(self) -> str:
        return random.choice(self.word_list)


def create_app() -> tornado.web.Application:
    return tornado.web.Application(
        [(r"/websocket/", WebSocketServer)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )


def main() -> None:
    app = create_app()
    app.listen(8888)
    io_loop = tornado.ioloop.IOLoop.current()

    word_selector = RandomWordSelector(["apple", "banana", "orange", "grape", "melon"])
    periodic_callback = tornado.ioloop.PeriodicCallback(
        lambda: WebSocketServer.send_message(word_selector.sample()),
        3000,
    )
    periodic_callback.start()

    io_loop.start()


if __name__ == "__main__":
    main()
