import os
import yaml
from urllib.parse import urlparse, ParseResult
from pathlib import Path
from typing import Any, Dict, List
from .constants import DIRECT_FILE_LINK_URL


def load_config(path: str) -> Any:

    """ Return downloaded yml config, which is specified app configuration
    For instance: host, port and e.t.c

    >>> from pathlib import Path, PosixPath
    >>> PROJECT_ROOT: PosixPath = Path(__file__).parent.parent
    >>> config: Dict = load_config(PROJECT_ROOT / "configs" / "base.yaml")
    >>> isinstance(config, dict)
    False
    """

    with Path(path).open() as fp:
        return yaml.safe_load(fp.read())


def read_env_variable(variable: str) -> Any:

    """ Return specified environment variable

    >>> os.environ["BOT_TOKEN"] = "TEST_TOKEN123"
    >>> var: str = read_env_variable("BOT_TOKEN")
    >>> var
    'TEST_TOKEN123'
    """

    value: Any = os.environ.get(variable)
    if value is None:
        raise RuntimeError(f"{variable} is required to start the service!")
    return value


def get_file_id(url: str) -> str:

    """ Return unique file id, which is hosted by slack.

    >>> file_url: str = "https://files.slack.com/files-pri/T02V3SQNKHQ-F032PK3KG3B/macbook.jpeg?pub_secret=84e22a0b2f"
    >>> file_id: str = get_file_id(file_url)
    >>> file_id
    'F032PK3KG3B'
    """

    file_id: str
    team_and_file_id: str
    parse_result: ParseResult = urlparse(url)
    splitted_path: List[str] = parse_result.path.split('/')
    _, _files_pri, team_and_file_id, _file_name = splitted_path
    _team_id, file_id = team_and_file_id.split('-')
    return file_id


def create_image_direct_url(file_info: Dict) -> str:

    """ Return image url, which can be downloaded within image ui block.
    Direct link format requires 3 attributes: team_id, file_id, pub_secret:
    https://files.slack.com/files-pri/{team_id}-{file_id}/macbook.jpeg?pub_secret={pub_secret}

    >>> file_info: Dict = {'file': {'name': 'macbook.jpeg', 'permalink_public': 'https://slack-files.com/T02V3SQNKHQ-F0330UENQQY-906fb6c2cb'}}
    >>> direct_url: str = create_image_direct_url(file_info)
    >>> direct_url
    'https://files.slack.com/files-pri/T02V3SQNKHQ-F0330UENQQY/macbook.jpeg?pub_secret=906fb6c2cb'
    """

    team_id: str
    file_id: str
    pub_secret: str
    filename: str = file_info['file']['name']
    url_parsed: ParseResult = urlparse(file_info['file']['permalink_public'])
    team_id, file_id, pub_secret = url_parsed.path.split('-')
    return f'{DIRECT_FILE_LINK_URL}{team_id}-{file_id}/{filename}?pub_secret={pub_secret}'


if __name__ == "__main__":

    """
    python3 -m app.utils
    """
    
    import doctest
    doctest.testmod()