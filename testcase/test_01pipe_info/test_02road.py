import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("路段信息")
class TestRoad(basecase.BaseCase):

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

    @allure.story("查看路段信息界面")
    def test_get_road(self):
        para = {"pageNum": 1, "pageSize": 10}
        ret = self.req_by_test('get_road', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  

    @allure.story("新增路段信息")
    def test_add_road(self):
        para = {
            "ggMc": "road",
            "utid": "63",
            "utConinfo": {
                "adName": "test"
            }
            }
        self.req_by_test('add_road', self.api_data, para)
        para = {"pageNum": 1, "pageSize": 10, "ggMc": "road"}
        ret = self.req_by_test('search_road', self.api_data, para)
        for i in ret['rows']:
            if i['ggMc']=='road':
                TestRoad.road_id = i['id']
        assert TestRoad.road_id != None, "未获取到新增路段信息的ID，新增失败"

    @allure.story("查看指定路段信息")
    def test_view_road_by_id(self):
        ret = self.req_by_test('view_road', self.api_data, add_url=self.road_id)
        assert "road" in ret["data"]["ggMc"], "查询结果为空"  
    
    @allure.story("修改指定路段信息")
    def test_modify_road_by_id(self):
        ret = self.req_by_test('view_road', self.api_data, add_url=self.road_id)
        data = ret['data']
        data['jj'] = "test"
        self.req_by_test('modify_road', self.api_data, data)
        ret = self.req_by_test('view_road', self.api_data, add_url=self.road_id)
        assert ret['data']['jj'] == "test", "确认修改失败"

    @allure.story("搜索指定路段信息")
    def test_search_road_by_name(self):
        para = {"pageNum": 1, "pageSize": 10, "ggMc": "road"}
        ret = self.req_by_test('search_road', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1, "pageSize": 10, "ggMc": "testXXX"}
        ret = self.req_by_test('search_road', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.story("导出所有路段信息")
    def test_export_road(self):
        for api in self.api_data:
            if api['api_name'] in "export_road":
                ret = self.session.download_file(api['req'], api['method'], filename='road.csv')

    @allure.story("删除指定路段信息")
    def test_delete_road_by_id(self):
        self.req_by_test('delete_road', self.api_data, add_url=self.road_id)
        para = {"pageNum": 1, "pageSize": 10, "ggMc": "road"}
        ret = self.req_by_test('search_road', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    