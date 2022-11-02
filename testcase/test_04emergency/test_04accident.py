import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("事故登记")
class TestAccident(basecase.BaseCase):


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

    @allure.story("查看事故登记界面")
    def test_get_accident(self):
        para = {"pageNum": 1,"pageSize": 10}
        ret = self.req_by_test('get_accident', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  
    
    @allure.story("新增事故登记")
    def test_add_accident(self):
        para = {
            "accidentName": "accident",
            "happenTime": "2022-10-19",
            "findTime": "2022-10-19",
            "happenLocationId": "test",
            "accidentLevel": "1",
            "accidentType": "1",
            "accidentProp": "1",
            "accidentFacilities": "1",
            "accidentReason": "test",
            "emerplanid": "20",
            "emerPlanName": "1",
            "countManager": "test",
            "reportDate": "2022-10-18",
            "position": "test",
            }
        self.req_by_test('add_accident', self.api_data, para)
        para = {"pageNum": 1,"pageSize": 10, "accidentName": "accident"}
        ret = self.req_by_test('search_accident', self.api_data, para)
        for i in ret['rows']:
            if i['accidentName']=='accident':
                TestAccident.accident_id = i['id']
        assert TestAccident.accident_id != None, "未获取到新增事故登记的ID，新增失败"

    @allure.story("查看指定事故登记")
    def test_view_accident_by_id(self):
        ret = self.req_by_test('view_accident', self.api_data, add_url=self.accident_id)
        assert "accident" in ret["data"]["accidentName"], "查询结果为空"  

    @allure.story("修改指定事故登记")
    def test_modify_accident_by_id(self):
        ret = self.req_by_test('view_accident', self.api_data, add_url=self.accident_id)
        data = ret['data']
        data['accidentLevel'] = "2"
        ret = self.req_by_test('modify_accident', self.api_data, data)
        ret = self.req_by_test('view_accident', self.api_data, add_url=self.accident_id)
        assert ret['data']['accidentLevel'] == "2", "确认修改失败"

    @allure.story("查询指定事故登记")
    def test_search_accident_by_name(self):
        para = {"pageNum": 1,"pageSize": 10, "accidentName": "accident"}
        ret = self.req_by_test('search_accident', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1,"pageSize": 10, "accidentName": "testXXX"}
        ret = self.req_by_test('search_accident', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.story("导出所有事故登记")
    def test_export_accident(self):
        for api in self.api_data:
            if api['api_name'] in "export_accident":
                ret = self.session.download_file(api['req'], api['method'], filename='accident.csv')

    @allure.story("删除指定事故登记")
    def test_delete_accident_by_id(self):
        self.req_by_test('delete_accident', self.api_data, add_url=self.accident_id)
        para = {"pageNum": 1,"pageSize": 10, "accidentName": "accident"}
        ret = self.req_by_test('search_accident', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

