import sys
import pytest

class BaseCase(object):
    session = None
    api_data = None

    @pytest.fixture(scope="class", autouse=True)
    @pytest.mark.usefixtures('get_session','get_api')
    def origin(self, get_session, get_api):
        BaseCase.session = get_session
        BaseCase.api_data = get_api
        