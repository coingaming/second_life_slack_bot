import logging
from aiohttp import web
from slack_bolt.app.async_server import AsyncSlackAppServer
from slack_bolt.util.utils import get_boot_message
from typing import NoReturn


class SecondlifeAppServer(AsyncSlackAppServer):
    def __init__(
        self,
        host: str,
        port: int,
        path: str,
        app: "AsyncApp",
    ):
        super(SecondlifeAppServer, self).__init__(port, path, app)
        self.host = host

    def start(self) -> NoReturn:
        if self.bolt_app.logger.level > logging.INFO:
            print(get_boot_message())
        else:
            self.bolt_app.logger.info(get_boot_message())
        web.run_app(self.web_app, host=self.host, port=self.port)