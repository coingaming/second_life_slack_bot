from aiohttp import web
from typing import Dict, NoReturn
from .async_server import SecondlifeAppServer
from .async_app import SecondlifeBotApp
from .settings import BOT_SLACK_TOKEN, SIGNING_SLACK_SECRET, PROJECT_ROOT
from .handlers import setup_requests_handlers
from .utils import load_config


async def get_web_app():

    """
        An entry point for web services (gunicorn e.t.c) 
    """

    config: Dict = load_config(PROJECT_ROOT / "configs" / "base.yaml")
    app: SecondlifeBotApp = SecondlifeBotApp(
        signing_secret=SIGNING_SLACK_SECRET,
        token=BOT_SLACK_TOKEN
    )
    setup_requests_handlers(app, config)
    server: SecondlifeAppServer = SecondlifeAppServer(
        host=config["host"], 
        port=config["port"],
        path=config['request_url'],
        app=app
    )
    return server.web_app


def start_bolt_app() -> NoReturn:

    """
        Function launches bolt application https://slack.dev/bolt-python/api-docs/slack_bolt/
        For development purposes only
    """

    config: Dict = load_config(PROJECT_ROOT / "configs" / "base.yaml")
    app: SecondlifeBotApp = SecondlifeBotApp(
        signing_secret=SIGNING_SLACK_SECRET,
        token=BOT_SLACK_TOKEN
    )
    setup_requests_handlers(app, config)
    server: SecondlifeAppServer = SecondlifeAppServer(
        host=config["host"], 
        port=config["port"],
        path=config['request_url'],
        app=app
    )
    app.start(server=server)