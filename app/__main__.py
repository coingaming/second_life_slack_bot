from typing import Dict
from .async_server import SecondlifeAppServer
from .async_app import SecondlifeBotApp
from .settings import BOT_SLACK_TOKEN, SIGNING_SLACK_SECRET, PROJECT_ROOT
from .handlers import setup_requests_handlers
from .utils import load_config


if __name__ == "__main__":
    config: Dict = load_config(PROJECT_ROOT / "configs" / "base.yaml")
    app: SecondlifeBotApp = SecondlifeBotApp(
        signing_secret=SIGNING_SLACK_SECRET,
        token=BOT_SLACK_TOKEN
    )
    server: SecondlifeAppServer = SecondlifeAppServer(
        host=config["host"], 
        port=config["port"],
        path=config['request_url'],
        app=app
    )
    setup_requests_handlers(app, config)
    app.start(server=server)