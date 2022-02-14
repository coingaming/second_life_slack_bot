from pathlib import Path, PosixPath
from .utils import read_env_variable


PROJECT_ROOT: PosixPath = Path(__file__).parent.parent

BOT_SLACK_TOKEN: str = read_env_variable("BOT_SLACK_TOKEN")

APP_SLACK_TOKEN: str = read_env_variable("APP_SLACK_TOKEN")

SIGNING_SLACK_SECRET: str = read_env_variable("SIGNING_SLACK_SECRET")
