from slack_bolt.app.async_app import AsyncApp
from slack_bolt.app.async_server import AsyncSlackAppServer
from typing import NoReturn

class SecondlifeBotApp(AsyncApp):

    def start(self, server: AsyncSlackAppServer) -> NoReturn:
        if self._server is None:
            self._server = server
        self._server.start()