import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("报警设置")
class TestAlarmSet(basecase.BaseCase):


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

    @allure.story("查看报警设置界面")
    def test_get_alarmset(self):
        para = {"pageNum": 1,"pageSize": 10}
        ret = self.req_by_test('get_alarmset', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  
    
    @pytest.mark.skip(reason="受限于查询条件")
    @allure.story("新增报警设置")
    def test_add_alarmset(self):
        para = {
            "paramTypeid": "948bcbcce9b94c30a7a3753ae916c514",
            "enableAlarm": "1",
            "valueAlarm": "1",
            "nomalValue": "0",
            "valueRespond": "1",
            "valuePriority": "2",
            "normalColor": "2",
            }
        self.req_by_test('add_alarmset', self.api_data, para)
        para = {"isshow": 1, "name": "alarmset"}
        ret = self.req_by_test('search_alarmset', self.api_data, para)
        for i in ret['data']:
            if i['name']=='alarmset':
                TestAlarmSet.alarmset_id = i['id']
        assert TestAlarmSet.alarmset_id != None, "未获取到新增报警设置的ID，新增失败"

    @pytest.mark.skip(reason="受限于查询条件")
    @allure.story("查看指定报警设置")
    def test_view_alarmset_by_id(self):
        ret = self.req_by_test('view_alarmset', self.api_data, add_url=self.alarmset_id)
        assert "alarmset" in ret["data"]["name"], "查询结果为空"  

    @pytest.mark.skip(reason="受限于查询条件")
    @allure.story("修改指定报警设置")
    def test_modify_alarmset_by_id(self):
        ret = self.req_by_test('view_alarmset', self.api_data, add_url=self.alarmset_id)
        data = ret['data']
        data['sort'] = 5
        ret = self.req_by_test('modify_alarmset', self.api_data, data)
        ret = self.req_by_test('view_alarmset', self.api_data, add_url=self.alarmset_id)
        assert ret['data']['sort'] == 5, "确认修改失败"

    @pytest.mark.skip(reason="受限于查询条件")
    @allure.story("查询指定报警设置")
    def test_search_alarmset_by_name(self):
        para = {"isshow": 1, "name": "alarmset"}
        ret = self.req_by_test('search_alarmset', self.api_data, para)
        assert len(ret['data'] ) == 1, "搜索返回结果数目不为1"
        para = {"isshow": 1, "name": "testXXX"}
        ret = self.req_by_test('search_alarmset', self.api_data, para)
        assert len(ret['data'] ) == 0, "搜索返回结果数目不为0"

    @allure.story("导出所有报警设置")
    def test_export_alarmset(self):
        for api in self.api_data:
            if api['api_name'] in "export_alarmset":
                ret = self.session.download_file(api['req'], api['method'], filename='alarmset.csv')

    @pytest.mark.skip(reason="受限于查询条件")
    @allure.story("删除指定报警设置")
    def test_delete_alarmset_by_id(self):
        self.req_by_test('delete_alarmset', self.api_data, add_url=self.alarmset_id)
        para = {"isshow": 1, "name": "alarmset"}
        ret = self.req_by_test('search_alarmset', self.api_data, para)
        assert len(ret['data'] ) == 0, "搜索返回结果数目不为0,删除失败"    

