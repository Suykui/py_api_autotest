import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("投料口信息")
class TestFeeding(basecase.BaseCase):

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

    @allure.feature("查看投料口信息界面")
    def test_get_feeding(self):
        para = {"pageNum": 1, "pageSize": 10}
        ret = self.req_by_test('get_feeding', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  

    @allure.feature("新增投料口信息")
    def test_add_feeding(self):
        para = {
            "fhfqid": "0a74d18e240440a1961a85353b407e5f13_F596293104054081956EA17A791A0D34",
            "tlkmc": "feeding",
            "utid": "F596293104054081956EA17A791A0D34",
            "fhfqName": "江山路103分区给水舱",
            "utName": "江山路",
            "ggMc": "江山路",
            "ggDm": "370050dcb35f465ea80c579fb5c1d1b41_F596293104054081956EA17A791A0D34"
            }
        self.req_by_test('add_feeding', self.api_data, para)
        para = {"pageNum": 1, "pageSize": 10, "tlkmc": "feeding"}
        ret = self.req_by_test('search_feeding', self.api_data, para)
        for i in ret['rows']:
            if i['tlkmc']=='feeding':
                TestFeeding.feeding_id = i['id']
        assert TestFeeding.feeding_id != None, "未获取到新增投料口的ID，新增失败"

    @allure.feature("查看指定投料口信息")
    def test_view_feeding_by_id(self):
        ret = self.req_by_test('view_feeding', self.api_data, add_url=self.feeding_id)
        assert "feeding" in ret["data"]["tlkmc"], "查询结果为空"  
    
    @allure.feature("修改指定投料口信息")
    def test_modify_feeding_by_id(self):
        ret = self.req_by_test('view_feeding', self.api_data, add_url=self.feeding_id)
        data = ret['data']
        data['cd'] = '5'
        ret = self.req_by_test('modify_feeding', self.api_data, data)
        ret = self.req_by_test('view_feeding', self.api_data, add_url=self.feeding_id)
        assert ret['data']['cd'] == '5', "确认修改失败"

    @allure.feature("搜索指定投料口信息")
    def test_search_feeding_by_name(self):
        para = {"pageNum": 1, "pageSize": 10, "tlkmc": "feeding"}
        ret = self.req_by_test('search_feeding', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1, "pageSize": 10, "tlkmc": "testXXX"}
        ret = self.req_by_test('search_feeding', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.feature("导出所有投料口信息")
    def test_export_feeding(self):
        for api in self.api_data:
            if api['api_name'] in "export_feeding":
                ret = self.session.download_file(api['req'], api['method'], filename='feeding.csv')

    @allure.feature("删除指定投料口信息")
    def test_delete_feeding_by_id(self):
        self.req_by_test('delete_feeding', self.api_data, add_url=self.feeding_id)
        para = {"pageNum": 1, "pageSize": 10, "tlkmc": "feeding"}
        ret = self.req_by_test('search_feeding', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

