import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("集水坑信息")
class TestPuddle(basecase.BaseCase):

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

    @allure.feature("查看集水坑信息界面")
    def test_get_puddle(self):
        para = {"pageNum": 1, "pageSize": 10}
        ret = self.req_by_test('get_puddle', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  

    @allure.feature("新增集水坑信息")
    def test_add_puddle(self):
        para = {
            "fhfqid": "0a74d18e240440a1961a85353b407e5f13_F596293104054081956EA17A791A0D34",
            "jskmc": "puddle",
            "utid": "F596293104054081956EA17A791A0D34",
            "fhfqName": "江山路103分区给水舱",
            "utName": "江山路",
            "ggMc": "江山路",
            "ggDm": "370050dcb35f465ea80c579fb5c1d1b41_F596293104054081956EA17A791A0D34"
            }
        self.req_by_test('add_puddle', self.api_data, para)
        para = {"pageNum": 1, "pageSize": 10, "jskmc": "puddle"}
        ret = self.req_by_test('search_puddle', self.api_data, para)
        for i in ret['rows']:
            if i['jskmc']=='puddle':
                TestPuddle.puddle_id = i['id']
        assert TestPuddle.puddle_id != None, "未获取到新增出入口的ID，新增失败"

    @allure.feature("查看指定集水坑信息")
    def test_view_puddle_by_id(self):
        ret = self.req_by_test('view_puddle', self.api_data, add_url=self.puddle_id)
        assert "puddle" in ret["data"]["jskmc"], "查询结果为空"  
    
    @allure.feature("修改指定集水坑信息")
    def test_modify_puddle_by_id(self):
        ret = self.req_by_test('view_puddle', self.api_data, add_url=self.puddle_id)
        data = ret['data']
        data['cd'] = 5
        ret = self.req_by_test('modify_puddle', self.api_data, data)
        ret = self.req_by_test('view_puddle', self.api_data, add_url=self.puddle_id)
        assert ret['data']['cd'] == 5, "确认修改失败"

    @allure.feature("搜索指定集水坑信息")
    def test_search_puddle_by_name(self):
        para = {"pageNum": 1, "pageSize": 10, "jskmc": "puddle"}
        ret = self.req_by_test('search_puddle', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1, "pageSize": 10, "jskmc": "testXXX"}
        ret = self.req_by_test('search_puddle', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.feature("导出所有集水坑信息")
    def test_export_puddle(self):
        for api in self.api_data:
            if api['api_name'] in "export_puddle":
                ret = self.session.download_file(api['req'], api['method'], filename='puddle.csv')

    @allure.feature("删除指定集水坑信息")
    def test_delete_puddle_by_id(self):
        self.req_by_test('delete_puddle', self.api_data, add_url=self.puddle_id)
        para = {"pageNum": 1, "pageSize": 10, "jskmc": "puddle"}
        ret = self.req_by_test('search_puddle', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

