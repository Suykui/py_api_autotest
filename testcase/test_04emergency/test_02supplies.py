import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("应急物资")
class TestSupplies(basecase.BaseCase):

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

    @allure.story("查看应急物资界面")
    def test_get_supplies(self):
        para = {"pageNum": 1,"pageSize": 10}
        ret = self.req_by_test('get_supplies', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  
    
    @allure.story("新增应急物资")
    def test_add_supplies(self):
        para = {
            "resName": "supplies",
            "resType": "0",
            "utid": "F596293104054081956EA17A791A0D34",
            "utconEmergencyResRefList": []
            }
        self.req_by_test('add_supplies', self.api_data, para)
        para = {"pageNum": 1,"pageSize": 10, "resName": "supplies"}
        ret = self.req_by_test('search_supplies', self.api_data, para)
        for i in ret['rows']:
            if i['resName']=='supplies':
                TestSupplies.supplies_id = i['id']
        assert TestSupplies.supplies_id != None, "未获取到新增应急物资的ID，新增失败"

    @allure.story("查看指定应急物资")
    def test_view_supplies_by_id(self):
        ret = self.req_by_test('view_supplies', self.api_data, add_url=self.supplies_id)
        assert "supplies" in ret["data"]["resName"], "查询结果为空"  

    @allure.story("修改指定应急物资")
    def test_modify_supplies_by_id(self):
        ret = self.req_by_test('view_supplies', self.api_data, add_url=self.supplies_id)
        data = ret['data']
        data['model'] = "test"
        ret = self.req_by_test('modify_supplies', self.api_data, data)
        ret = self.req_by_test('view_supplies', self.api_data, add_url=self.supplies_id)
        assert ret['data']['model'] == "test", "确认修改失败"

    @allure.story("查询指定应急物资")
    def test_search_supplies_by_name(self):
        para = {"pageNum": 1,"pageSize": 10, "resName": "supplies"}
        ret = self.req_by_test('search_supplies', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1,"pageSize": 10, "resName": "testXXX"}
        ret = self.req_by_test('search_supplies', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.story("导出所有应急物资")
    def test_export_supplies(self):
        for api in self.api_data:
            if api['api_name'] in "export_supplies":
                ret = self.session.download_file(api['req'], api['method'], filename='supplies.csv')

    @allure.story("删除指定应急物资")
    def test_delete_supplies_by_id(self):
        self.req_by_test('delete_supplies', self.api_data, add_url=self.supplies_id)
        para = {"pageNum": 1,"pageSize": 10, "resName": "supplies"}
        ret = self.req_by_test('search_supplies', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

