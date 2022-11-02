from multiprocessing.forkserver import read_signed
import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("出入口信息")
class TestInout(basecase.BaseCase):

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

    @allure.story("查看出入口信息界面")
    def test_get_inout(self):
        para = {"pageNum": 1, "pageSize": 10}
        ret = self.req_by_test('get_inout', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  

    @allure.story("新增出入口信息")
    def test_add_inout(self):
        para = {
            "crkmc": "inout",
            "fhfqid": "910680c3fbac4a469da744d5ece625bc1_F596293104054081956EA17A791A0D34",
            "utid": "F596293104054081956EA17A791A0D34",
            "fhfqName": "前港湾路204分区给信舱",
            "utName": "江山路",
            "ggDm": "370050dcb35f465ea80c579fb5c1d1b41_F596293104054081956EA17A791A0D34",
            "ggMc": "江山路"
            }
        self.req_by_test('add_inout', self.api_data, para)
        para = {"pageNum": 1, "pageSize": 10, "crkmc": "inout"}
        ret = self.req_by_test('search_inout', self.api_data, para)
        for i in ret['rows']:
            if i['crkmc']=='inout':
                TestInout.inout_id = i['id']
        assert TestInout.inout_id != None, "未获取到新增出入口的ID，新增失败"

    @allure.story("查看指定出入口信息")
    def test_view_inout_by_id(self):
        ret = self.req_by_test('view_inout', self.api_data, add_url=self.inout_id)
        assert "inout" in ret["data"]["crkmc"], "查询结果为空"  
    
    @allure.story("修改指定出入口信息")
    def test_modify_inout_by_id(self):
        ret = self.req_by_test('view_inout', self.api_data, add_url=self.inout_id)
        data = ret['data']
        data['crksize'] = '5'
        ret = self.req_by_test('modify_inout', self.api_data, data)
        ret = self.req_by_test('view_inout', self.api_data, add_url=self.inout_id)
        assert ret['data']['crksize'] == '5', "确认修改失败"
    
    @allure.story("搜索指定出入口信息")
    def test_search_inout_by_name(self):
        para = {"pageNum": 1, "pageSize": 10, "crkmc": "inout"}
        ret = self.req_by_test('search_inout', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1, "pageSize": 10, "crkmc": "testXXX"}
        ret = self.req_by_test('search_inout', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.story("导出所有出入口信息")
    def test_export_inout(self):
        for api in self.api_data:
            if api['api_name'] in "export_inout":
                ret = self.session.download_file(api['req'], api['method'], filename='inout.csv')

    @allure.story("删除指定出入口信息")
    def test_delete_inout_by_id(self):
        self.req_by_test('delete_inout', self.api_data, add_url=self.inout_id)
        para = {"pageNum": 1, "pageSize": 10, "crkmc": "inout"}
        ret = self.req_by_test('search_inout', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

