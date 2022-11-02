import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("设备类型")
class TestEquType(basecase.BaseCase):


    def setup_method(self, method):
        logger.info("------------------%s start ------------------" % method.__name__)

    def teardown_method(self, method):
        logger.info("------------------%s end ------------------" % method.__name__)

    def req_by_test(self, action, api_data, para=None, add_url=None):
        ret = None
        for api in api_data:
            if api['api_name'] in action:
                if add_url:
                    ret = self.session.check_req(api['req']+add_url, api['method'], payload=para)
                else:
                    ret = self.session.check_req(api['req'], api['method'], payload=para)
        assert ret != None, "请求失败"
        return ret

    @allure.feature("查看设备类型界面")
    def test_get_equtype(self):
        para = {"isshow": 1}
        ret = self.req_by_test('get_equtype', self.api_data, para)
        assert len(ret["data"]) != 0, "查询结果为空"  

    @allure.feature("新增设备类型")
    def test_add_equtype(self):
        para = {
            "name": "equtype",
            "parentId": 0,
            "sort": 0,
            "dname": "equtype",
            "isshow": "1",
            "type": "1",
            }
        self.req_by_test('add_equtype', self.api_data, para)
        para = {"isshow": 1, "name": "equtype"}
        ret = self.req_by_test('search_equtype', self.api_data, para)
        for i in ret['data']:
            if i['name']=='equtype':
                TestEquType.equtype_id = i['id']
        assert TestEquType.equtype_id != None, "未获取到新增设备类型的ID，新增失败"

    @allure.feature("查看指定设备类型")
    def test_view_equtype_by_id(self):
        ret = self.req_by_test('view_equtype', self.api_data, add_url=self.equtype_id)
        assert "equtype" in ret["data"]["name"], "查询结果为空"  

    @allure.feature("修改指定设备类型")
    def test_modify_equtype_by_id(self):
        ret = self.req_by_test('view_equtype', self.api_data, add_url=self.equtype_id)
        data = ret['data']
        data['sort'] = 5
        ret = self.req_by_test('modify_equtype', self.api_data, data)
        ret = self.req_by_test('view_equtype', self.api_data, add_url=self.equtype_id)
        assert ret['data']['sort'] == 5, "确认修改失败"

    @allure.feature("搜索指定设备类型")
    def test_search_equtype_by_name(self):
        para = {"isshow": 1, "name": "equtype"}
        ret = self.req_by_test('search_equtype', self.api_data, para)
        assert len(ret['data'] ) == 1, "搜索返回结果数目不为1"
        para = {"isshow": 1, "name": "testXXX"}
        ret = self.req_by_test('search_equtype', self.api_data, para)
        assert len(ret['data'] ) == 0, "搜索返回结果数目不为0"

    @pytest.mark.skip(reason="没有导出功能")
    @allure.feature("导出所有设备类型")
    def test_export_equtype(self):
        for api in self.api_data:
            if api['api_name'] in "export_equtype":
                ret = self.session.download_file(api['req'], api['method'], filename='equtype.csv')

    @allure.feature("删除指定设备类型")
    def test_delete_equtype_by_id(self):
        self.req_by_test('delete_equtype', self.api_data, add_url=self.equtype_id)
        para = {"isshow": 1, "name": "equtype"}
        ret = self.req_by_test('search_equtype', self.api_data, para)
        assert len(ret['data'] ) == 0, "搜索返回结果数目不为0,删除失败"    

