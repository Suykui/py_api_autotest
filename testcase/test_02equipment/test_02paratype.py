import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("参数类型")
class TestParaType(basecase.BaseCase):

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

    @allure.story("查看参数类型界面")
    def test_get_paratype(self):
        para = {"pageNum": 1,"pageSize": 10}
        ret = self.req_by_test('get_paratype', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  

    @allure.story("新增参数类型")
    def test_add_paratype(self):
        para = {
            "typeName": "paratype",
            "controlType": "1",
            "numberType": "1",
            "alarmType": "1",
            }
        self.req_by_test('add_paratype', self.api_data, para)
        para = {"pageNum": 1,"pageSize": 10, "typeName": "paratype"}
        ret = self.req_by_test('search_paratype', self.api_data, para)
        for i in ret['rows']:
            if i['typeName']=='paratype':
                TestParaType.paratype_id = i['id']
        assert TestParaType.paratype_id != None, "未获取到新增参数类型的ID，新增失败"

    @allure.story("查看指定参数类型")
    def test_view_paratype_by_id(self):
        ret = self.req_by_test('view_paratype', self.api_data, add_url=self.paratype_id)
        assert "paratype" in ret["data"]["typeName"], "查询结果为空"  

    @allure.story("修改指定参数类型")
    def test_modify_paratype_by_id(self):
        ret = self.req_by_test('view_paratype', self.api_data, add_url=self.paratype_id)
        data = ret['data']
        data['alarmType'] = "2"
        ret = self.req_by_test('modify_paratype', self.api_data, data)
        ret = self.req_by_test('view_paratype', self.api_data, add_url=self.paratype_id)
        assert ret['data']['alarmType'] == "2", "确认修改失败"

    @allure.story("搜索指定参数类型")
    def test_search_paratype_by_name(self):
        para = {"pageNum": 1,"pageSize": 10, "typeName": "paratype"}
        ret = self.req_by_test('search_paratype', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1,"pageSize": 10, "typeName": "testXXX"}
        ret = self.req_by_test('search_paratype', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.story("导出所有参数类型")
    def test_export_paratype(self):
        for api in self.api_data:
            if api['api_name'] in "export_paratype":
                ret = self.session.download_file(api['req'], api['method'], filename='paratype.csv')

    @allure.story("删除指定参数类型")
    def test_delete_paratype_by_id(self):
        self.req_by_test('delete_paratype', self.api_data, add_url=self.paratype_id)
        para = {"pageNum": 1,"pageSize": 10, "typeName": "paratype"}
        ret = self.req_by_test('search_paratype', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

