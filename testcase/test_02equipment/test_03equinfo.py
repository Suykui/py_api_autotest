import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("设备基础信息")
class TestEquInfo(basecase.BaseCase):

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

    @allure.story("查看设备基础信息界面")
    def test_get_equinfo(self):
        para = {"pageNum": 1,"pageSize": 10}
        ret = self.req_by_test('get_equinfo', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  

    @allure.story("新增设备基础信息")
    def test_add_equinfo(self):
        para = {
            "equipmentName": "equinfo",
            "equipmentTypeid": "a00af48f770e46c6ae6655c5971d33d4",
            "state": "0",
            "fhfqDm": "910680c3fbac4a469da744d5ece625bc1_F596293104054081956EA17A791A0D34",
            "utid": "F596293104054081956EA17A791A0D34",
            }
        self.req_by_test('add_equinfo', self.api_data, para)
        para = {"pageNum": 1,"pageSize": 10, "equipmentName": "equinfo"}
        ret = self.req_by_test('search_equinfo', self.api_data, para)
        for i in ret['rows']:
            if i['equipmentName']=='equinfo':
                TestEquInfo.equinfo_id = i['id']
        assert TestEquInfo.equinfo_id != None, "未获取到新增设备基础信息的ID，新增失败"

    @allure.story("查看指定设备基础信息")
    def test_view_equinfo_by_id(self):
        ret = self.req_by_test('view_equinfo', self.api_data, add_url=self.equinfo_id)
        assert "equinfo" in ret["data"]["equipmentName"], "查询结果为空"  
    
    @allure.story("修改指定设备基础信息")
    def test_modify_equinfo_by_id(self):
        ret = self.req_by_test('view_equinfo', self.api_data, add_url=self.equinfo_id)
        data = ret['data']
        data['state'] = "1"
        ret = self.req_by_test('modify_equinfo', self.api_data, data)
        ret = self.req_by_test('view_equinfo', self.api_data, add_url=self.equinfo_id)
        assert ret['data']['state'] == "1", "确认修改失败"
    
    @allure.story("搜索指定设备基础信息")
    def test_search_equinfo_by_name(self):
        para = {"pageNum": 1,"pageSize": 10, "equipmentName": "equinfo"}
        ret = self.req_by_test('search_equinfo', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1,"pageSize": 10, "equipmentName": "testXXX"}
        ret = self.req_by_test('search_equinfo', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @pytest.mark.skip(reason="有bug")
    @allure.story("导出所有设备信息")
    def test_export_equinfo(self):
        for api in self.api_data:
            if api['api_name'] in "export_equinfo":
                ret = self.session.download_file(api['req'], api['method'], filename='equinfo.csv')

    @allure.story("删除指定设备信息")
    def test_delete_equinfo_by_id(self):
        self.req_by_test('delete_equinfo', self.api_data, add_url=self.equinfo_id)
        para = {"pageNum": 1,"pageSize": 10, "equipmentName": "equinfo"}
        ret = self.req_by_test('search_equinfo', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

