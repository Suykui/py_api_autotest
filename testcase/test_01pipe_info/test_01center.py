import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("分控中心信息")
class TestCenter(basecase.BaseCase):
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

    @allure.story("查看分控中心信息界面")
    def test_get_center(self):
        para = {"pageNum": 1, "pageSize": 10}
        ret = self.req_by_test('get_center', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  

    @allure.story("新增分控中心")
    def test_add_center(self):
        para = {
            "adName": "auto_test",
            "conLength": "1",
            "totalInvestment": "1",
            "pipelineType": "1",
            "cabinType": "1",
            "longitude": "120",
            "latitude": "36",
            "sort": "0"
            }
        self.req_by_test('add_center', self.api_data, para)
        para = {"pageNum": 1, "pageSize": 10, "adName": "auto_test"}
        ret = self.req_by_test('search_center', self.api_data, para)
        for i in ret['rows']:
            if i['adName']=='auto_test':
                TestCenter.center_id = i['id']
        assert TestCenter.center_id != None, "未获取到新增分控中心的ID，新增失败"

    @allure.story("查看指定分控中心信息")
    def test_view_center_by_id(self):
        ret = self.req_by_test('view_center', self.api_data, add_url=self.center_id)
        assert "auto_test" in ret["data"]["adName"], "查询结果为空"  
    
    @allure.story("修改指定分控中心信息")
    def test_modify_center_by_id(self):
        ret = self.req_by_test('view_center', self.api_data, add_url=self.center_id)
        data = ret['data']
        data['cabinType'] = "1,2"
        data['pipelineType'] = "1,2"
        ret = self.req_by_test('modify_center', self.api_data, data)
        ret = self.req_by_test('view_center', self.api_data, add_url=self.center_id)
        assert ret['data']['cabinType'] == "1,2", "确认修改失败"
        assert ret['data']['pipelineType'] == "1,2", "确认修改失败"
    
    @allure.story("搜索指定分控中心信息")
    def test_search_center_by_name(self):
        para = {"pageNum": 1, "pageSize": 10, "adName": "auto_test"}
        ret = self.req_by_test('search_center', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1, "pageSize": 10, "adName": "testXXX"}
        ret = self.req_by_test('search_center', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.story("导出所有分控中心信息")
    def test_export_center(self):
        for api in self.api_data:
            if api['api_name'] in "export_center":
                ret = self.session.download_file(api['req'], api['method'], filename='center.csv')

    @allure.story("删除指定分控中心")
    def test_delete_center_by_id(self):
        self.req_by_test('delete_center', self.api_data, add_url=self.center_id)
        para = {"pageNum": 1, "pageSize": 10, "adName": "auto_test"}
        ret = self.req_by_test('search_center', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

