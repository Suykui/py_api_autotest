import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("分控中心事故管理")
class TestCenterAccident(basecase.BaseCase):


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

    @allure.story("查看分控中心事故管理界面")
    def test_get_centeraccident(self):
        para = {"pageNum": 1,"pageSize": 10}
        ret = self.req_by_test('get_centeraccident', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  
    
    @allure.story("新增分控中心事故管理")
    def test_add_centeraccident(self):
        para = {
            "accidentName": "centeraccident",
            "accidentLevel": "1",
            "accidentType": "1",
            "accidentProp": "1",
            }
        self.req_by_test('add_centeraccident', self.api_data, para)
        para = {"pageNum": 1,"pageSize": 10, "centeraccidentName": "centeraccident"}
        ret = self.req_by_test('search_centeraccident', self.api_data, para)
        for i in ret['rows']:
            if i['accidentName']=='centeraccident':
                TestCenterAccident.centeraccident_id = i['id']
        assert TestCenterAccident.centeraccident_id != None, "未获取到新增分控中心事故管理的ID，新增失败"

    @allure.story("查看指定分控中心事故管理")
    def test_view_centeraccident_by_id(self):
        ret = self.req_by_test('view_centeraccident', self.api_data, add_url=self.centeraccident_id)
        assert "centeraccident" in ret["data"]["accidentName"], "查询结果为空"  

    @allure.story("修改指定分控中心事故管理")
    def test_modify_centeraccident_by_id(self):
        ret = self.req_by_test('view_centeraccident', self.api_data, add_url=self.centeraccident_id)
        data = ret['data']
        data['accidentLevel'] = "2"
        ret = self.req_by_test('modify_centeraccident', self.api_data, data)
        ret = self.req_by_test('view_centeraccident', self.api_data, add_url=self.centeraccident_id)
        assert ret['data']['accidentLevel'] == "2", "确认修改失败"

    @allure.story("查询指定分控中心事故管理")
    def test_search_centeraccident_by_name(self):
        para = {"pageNum": 1,"pageSize": 10, "accidentName": "centeraccident"}
        ret = self.req_by_test('search_centeraccident', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1,"pageSize": 10, "accidentName": "testXXX"}
        ret = self.req_by_test('search_centeraccident', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.story("导出所有分控中心事故管理")
    def test_export_centeraccident(self):
        for api in self.api_data:
            if api['api_name'] in "export_centeraccident":
                ret = self.session.download_file(api['req'], api['method'], filename='centeraccident.csv')

    @allure.story("删除指定分控中心事故管理")
    def test_delete_centeraccident_by_id(self):
        self.req_by_test('delete_centeraccident', self.api_data, add_url=self.centeraccident_id)
        para = {"pageNum": 1,"pageSize": 10, "accidentName": "centeraccident"}
        ret = self.req_by_test('search_centeraccident', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

