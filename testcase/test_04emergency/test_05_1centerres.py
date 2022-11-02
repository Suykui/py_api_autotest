import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("分控中心应急物资")
class TestCenterRes(basecase.BaseCase):


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

    @allure.story("查看分控中心应急物资界面")
    def test_get_centerres(self):
        para = {"pageNum": 1,"pageSize": 10}
        ret = self.req_by_test('get_centerres', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  
    
    @allure.story("新增分控中心应急物资")
    def test_add_centerres(self):
        para = {
            "resName": "centerres",
            "resType": "0",
            "utid": "F596293104054081956EA17A791A0D34",
            "utconEmergencyResRefList": []
            }
        self.req_by_test('add_centerres', self.api_data, para)
        para = {"pageNum": 1,"pageSize": 10, "resName": "centerres"}
        ret = self.req_by_test('search_centerres', self.api_data, para)
        for i in ret['rows']:
            if i['resName']=='centerres':
                TestCenterRes.centerres_id = i['id']
        assert TestCenterRes.centerres_id != None, "未获取到新增分控中心应急物资的ID，新增失败"

    @allure.story("查看指定分控中心应急物资")
    def test_view_centerres_by_id(self):
        ret = self.req_by_test('view_centerres', self.api_data, add_url=self.centerres_id)
        assert "centerres" in ret["data"]["resName"], "查询结果为空"  

    @allure.story("修改指定分控中心应急物资")
    def test_modify_centerres_by_id(self):
        ret = self.req_by_test('view_centerres', self.api_data, add_url=self.centerres_id)
        data = ret['data']
        data['resType'] = "1"
        ret = self.req_by_test('modify_centerres', self.api_data, data)
        ret = self.req_by_test('view_centerres', self.api_data, add_url=self.centerres_id)
        assert ret['data']['resType'] == "1", "确认修改失败"

    @allure.story("查询指定分控中心应急物资")
    def test_search_centerres_by_name(self):
        para = {"pageNum": 1,"pageSize": 10, "resName": "centerres"}
        ret = self.req_by_test('search_centerres', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1,"pageSize": 10, "resName": "testXXX"}
        ret = self.req_by_test('search_centerres', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.story("导出所有分控中心应急物资")
    def test_export_centerres(self):
        for api in self.api_data:
            if api['api_name'] in "export_centerres":
                ret = self.session.download_file(api['req'], api['method'], filename='centerres.csv')

    @allure.story("删除指定分控中心应急物资")
    def test_delete_centerres_by_id(self):
        self.req_by_test('delete_centerres', self.api_data, add_url=self.centerres_id)
        para = {"pageNum": 1,"pageSize": 10, "resName": "centerres"}
        ret = self.req_by_test('search_centerres', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

