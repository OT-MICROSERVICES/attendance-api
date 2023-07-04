from flask import Flask
from flask_caching import Cache
import pytest

cache = Cache()

@pytest.fixture(scope='module')
def app():
    """Create a Flask app for testing"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['CACHE_TYPE'] = 'simple'
    cache.init_app(app)
    return app

def test_cache_set_get(app):
    # Set a value in the cache
    cache.set('key', 'value')

    # Get the value from the cache
    result = cache.get('key')

    # Assert the retrieved value
    assert result == 'value'


def test_cache_delete(app):
    # Set a value in the cache
    cache.set('key', 'value')

    # Delete the value from the cache
    cache.delete('key')

    # Get the value from the cache
    result = cache.get('key')

    # Assert that the value is None (deleted)
    assert result is None


def test_cache_clear(app):
    # Set values in the cache
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')

    # Clear the cache
    cache.clear()

    # Get the values from the cache
    result1 = cache.get('key1')
    result2 = cache.get('key2')

    # Assert that both values are None (cleared)
    assert result1 is None
    assert result2 is None


if __name__ == '__main__':
    pytest.main()
