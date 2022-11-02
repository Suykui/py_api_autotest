import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("应急预案")
class TestPlan(basecase.BaseCase):


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

    @allure.story("查看应急预案界面")
    def test_get_plan(self):
        para = {"pageNum": 1,"pageSize": 10}
        ret = self.req_by_test('get_plan', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  
    
    @allure.story("新增应急预案")
    def test_add_plan(self):
        para = {
            "emerPlanName": "plan",
            "accidentType": 1,
            "accidentLevel": 1,
            "accidentProp": 1,
            "emerPlanStepList": []
            }
        self.req_by_test('add_plan', self.api_data, para)
        para = {"pageNum": 1, "pageSize": 10, "emerPlanName": "plan"}
        ret = self.req_by_test('search_plan', self.api_data, para)
        for i in ret['rows']:
            if i['emerPlanName']=='plan':
                TestPlan.plan_id = i['id']
        assert TestPlan.plan_id != None, "未获取到新增应急预案的ID，新增失败"

    @allure.story("查看指定应急预案")
    def test_view_plan_by_id(self):
        ret = self.req_by_test('view_plan', self.api_data, add_url=self.plan_id)
        assert "plan" in ret["data"]["emerPlanName"], "查询结果为空"  

    @allure.story("修改指定应急预案")
    def test_modify_plan_by_id(self):
        ret = self.req_by_test('view_plan', self.api_data, add_url=self.plan_id)
        data = ret['data']
        data['accidentType'] = 2
        ret = self.req_by_test('modify_plan', self.api_data, data)
        ret = self.req_by_test('view_plan', self.api_data, add_url=self.plan_id)
        assert ret['data']['accidentType'] == 2, "确认修改失败"

    @allure.story("查询指定应急预案")
    def test_search_plan_by_name(self):
        para = {"pageNum": 1, "pageSize": 10, "emerPlanName": "plan"}
        ret = self.req_by_test('search_plan', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1, "pageSize": 10, "emerPlanName": "testXXX"}
        ret = self.req_by_test('search_plan', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.story("导出所有应急预案")
    def test_export_plan(self):
        for api in self.api_data:
            if api['api_name'] in "export_plan":
                ret = self.session.download_file(api['req'], api['method'], filename='plan.csv')

    @allure.story("删除指定应急预案")
    def test_delete_plan_by_id(self):
        self.req_by_test('delete_plan', self.api_data, add_url=self.plan_id)
        para = {"pageNum": 1, "pageSize": 10, "emerPlanName": "plan"}
        ret = self.req_by_test('search_plan', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

