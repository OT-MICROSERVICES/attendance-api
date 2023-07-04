import os
from unittest import mock
from client.redis import MiddlewareSDKFacade
from client.redis.redis_conn import get_caching_data

@mock.patch('client.redis.open')
def test_get_caching_data(mock_open):
    mock_file = mock.MagicMock()
    mock_file.__enter__.return_value = mock_file
    mock_file.read.return_value = """
    redis:
        host: localhost
        port: 6379
        password: mypassword
    """

    mock_open.return_value = mock_file
    os.environ['CONFIG_FILE'] = 'config.yaml'

    result = get_caching_data()

    assert result == {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_HOST": "172.17.0.4",
        "CACHE_REDIS_PORT": 6379,
        "CACHE_REDIS_URL": "redis://172.17.0.4:6379/0"
    }

    # mock_open.assert_called_once_with('config.yaml', 'r', encoding="utf-8")
    # mock_file.read.assert_called_once()
    #
    # del os.environ['CONFIG_FILE']


@mock.patch('client.redis.open')
def test_redis_status(mock_open):
    mock_file = mock.MagicMock()
    mock_file.__enter__.return_value = mock_file
    mock_file.read.return_value = """
    redis:
        host: localhost
        port: 6379
        password: mypassword
    """

    mock_open.return_value = mock_file
    os.environ['CONFIG_FILE'] = 'config.yaml'

    redis_client = MiddlewareSDKFacade.cache.redis_status()
    # mock_redis.assert_called_once_with(
    #     host="localhost",
    #     port=6379,
    #     password="mypassword",
    #     decode_responses=True
    # )
    assert redis_client == "up"

    del os.environ['CONFIG_FILE']