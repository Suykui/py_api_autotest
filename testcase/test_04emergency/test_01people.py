import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("应急人员")
class TestPeople(basecase.BaseCase):


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

    @allure.story("查看应急人员界面")
    def test_get_people(self):
        para = {"pageNum": 1, "pageSize": 10}
        ret = self.req_by_test('get_people', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  
    
    @allure.story("新增应急人员")
    def test_add_people(self):
        para = {
            "name": "people",
            "peopleType": "0",
            "holdPositions": "0",
            }
        self.req_by_test('add_people', self.api_data, para)
        para = {"pageNum": 1, "pageSize": 10, "name": "people"}
        ret = self.req_by_test('search_people', self.api_data, para)
        for i in ret['rows']:
            if i['name']=='people':
                TestPeople.people_id = i['id']
        assert TestPeople.people_id != None, "未获取到新增应急人员的ID，新增失败"

    @allure.story("查看指定应急人员")
    def test_view_people_by_id(self):
        ret = self.req_by_test('view_people', self.api_data, add_url=self.people_id)
        assert "people" in ret["data"]["name"], "查询结果为空"  

    @allure.story("修改指定应急人员")
    def test_modify_people_by_id(self):
        ret = self.req_by_test('view_people', self.api_data, add_url=self.people_id)
        data = ret['data']
        data['holdPositions'] = "1"
        ret = self.req_by_test('modify_people', self.api_data, data)
        ret = self.req_by_test('view_people', self.api_data, add_url=self.people_id)
        assert ret['data']['holdPositions'] == "1", "确认修改失败"

    @allure.story("查询指定应急人员")
    def test_search_people_by_name(self):
        para = {"pageNum": 1, "pageSize": 10,  "name": "people"}
        ret = self.req_by_test('search_people', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1, "pageSize": 10,  "name": "testXXX"}
        ret = self.req_by_test('search_people', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.story("导出所有应急人员")
    def test_export_people(self):
        for api in self.api_data:
            if api['api_name'] in "export_people":
                ret = self.session.download_file(api['req'], api['method'], filename='people.csv')

    @allure.story("删除指定应急人员")
    def test_delete_people_by_id(self):
        self.req_by_test('delete_people', self.api_data, add_url=self.people_id)
        para = {"pageNum": 1, "pageSize": 10, "name": "people"}
        ret = self.req_by_test('search_people', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

