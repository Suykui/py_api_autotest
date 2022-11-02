import os
import pytest
from utils.com_log import *
from conftest import config_data, api_data

param = []
ids = []
for data in api_data:

    if data != "login":
        param.extend(api_data[data])
        for req in api_data[data]:
            ids.append(data+"-"+req["api_name"])

@pytest.mark.parametrize('api_dict',param,ids=ids)
def test_api(get_session, api_dict):
    #logger.info(get_session.api_root_url)
    get_session.check_req(api_dict['req'], api_dict['method'], api_dict['payload'])

if __name__ == "__main__":
    #test_api()
    pytest.main(["-q", "-s", "test_api.py"])