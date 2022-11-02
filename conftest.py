import pytest
import json
import yaml
import sys
import os
from utils.com_session import ComSession
from utils.com_log import logger

path  = os.path.dirname(__file__)

def get_login_api():
    with open(path+'/api/login.json') as f:
        data = json.load(f)
        logger.info(data)
        print(data)
    return data

def get_config_data():
    with open(path+'/config/pipe_config.yaml') as f:
        data = yaml.safe_load(f)
        logger.info(data)
    return data

config_data = get_config_data()
api_login = get_login_api()

@pytest.fixture(scope="session", autouse=True)
def get_session():
    server_address = "http://" + str(config_data["server"]["ip"]) + ":" + \
        str(config_data["server"]["port"])
    login_url = api_login["login"]["req"]
    payload = {
        "username": str(config_data["account"]["user"]),
        "password": str(config_data["account"]["passwd"]),
        "rememberMe": False
        }
    session = ComSession(server_address, login_url, payload)
    yield session


@pytest.fixture(scope="class", autouse=True)
def get_api():
    full_name = os.environ.get('PYTEST_CURRENT_TEST').split(' ')[0]
    #logger.info(full_name)
    class_name = full_name.split("::")[1]
    logger.info("------------------%s start ------------------" %class_name)
    api_data = None
    for filepath, dirnames, filename in os.walk(os.path.join(os.path.dirname(__file__),'api')):
        for file in filename:
            if file[:-5] == class_name.lower()[4:]:
                logger.info("api file path:%s" % os.path.join(filepath, file))
                with open(os.path.join(filepath, file)) as f:
                    api_data = json.load(f)
                    logger.info("api data:%s" % api_data)

    yield api_data

    logger.info("------------------%s end ------------------" %class_name)
