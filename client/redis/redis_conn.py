"""
Module for Redis data and interface
"""
# pylint: disable=too-few-public-methods,no-member
import os
import redis
import yaml

CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.yaml')

def get_caching_data():
    """Function to get cache config for redis cache"""
    with open(CONFIG_FILE, 'r', encoding="utf-8") as config_file:
        yaml_value = yaml.load(config_file, Loader=yaml.FullLoader)
    config_dict={
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_HOST": yaml_value['redis']['host'],
        "CACHE_REDIS_PORT": yaml_value['redis']['port'],
        "CACHE_REDIS_URL": f"redis://{yaml_value['redis']['host']}:{yaml_value['redis']['port']}/0"
    }
    return config_dict


class CoreRedisClient:
    """Class for defining the structure of Redis database"""
    def __init__(self):
        with open(CONFIG_FILE, 'r', encoding="utf-8") as config_file:
            yaml_values = yaml.load(config_file, Loader=yaml.FullLoader)
        self.client = redis.Redis(host=yaml_values['redis']['host'],
                                   port=yaml_values['redis']['port'],
                                   password=yaml_values['redis']['password'],
                                   decode_responses=True)

    def redis_status(self):
        """Function for getting the health of redis"""
        try:
            self.client.ping()
            return "up"
        except redis.ConnectionError:
            return "down"
