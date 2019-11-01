import pytest
from urllib3.exceptions import MaxRetryError
from aqua.aqua import Aqua

from . import config


def test_valid_login():
    aqua = Aqua(id=config.username, password=config.password, host=config.host, port=config.port, using_tls=config.using_tls, verify_tls=config.verify_tls)
    assert aqua is not None
    assert aqua.token is not None
    assert aqua.id == 'username'
    assert aqua.port == 443
    assert aqua.api_version == 'v1'
    assert aqua.url_prefix == f"https://{config.host}:{config.port}/api/{aqua.api_version}"


def test_invalid_login():

    with pytest.raises(Exception) as excinfo:
        aqua = Aqua(id=config.username, password='incorrectpassword', host=config.host, port=config.port, using_tls=config.using_tls, verify_tls=config.verify_tls)

    assert excinfo.value.args[0] == 'Authentication Error'

