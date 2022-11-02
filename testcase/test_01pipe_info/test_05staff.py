import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("人员信息")
class TestStaff(basecase.BaseCase):

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

    @allure.feature("查看人员信息界面")
    def test_get_staff(self):
        para = {"pageNum": 1, "pageSize": 10}
        ret = self.req_by_test('get_staff', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  

    @allure.feature("新增人员信息")
    def test_add_staff(self):
        para = {
            "utid": "F596293104054081956EA17A791A0D34",
            "username": "staff",
            "usertype": "0",
            "userState": "1",
            "utName": "江山路"
            }
        self.req_by_test('add_staff', self.api_data, para)
        para = {"pageNum": 1, "pageSize": 10, "username": "staff",}
        ret = self.req_by_test('search_staff', self.api_data, para)
        for i in ret['rows']:
            if i['username']=='staff':
                TestStaff.staff_id = i['id']
        assert TestStaff.staff_id != None, "未获取到新增人员的ID，新增失败"

    @allure.feature("查看指定人员信息")
    def test_view_staff_by_id(self):
        ret = self.req_by_test('view_staff', self.api_data, add_url=self.staff_id)
        assert "staff" in ret["data"]["username"], "查询结果为空"  
    
    @allure.feature("修改指定人员信息")
    def test_modify_staff_by_id(self):
        ret = self.req_by_test('view_staff', self.api_data, add_url=self.staff_id)
        data = ret['data']
        data['usertype'] = "1"
        ret = self.req_by_test('modify_staff', self.api_data, data)
        ret = self.req_by_test('view_staff', self.api_data, add_url=self.staff_id)
        assert ret['data']['usertype'] == "1", "确认修改失败"
    
    @allure.feature("搜索指定人员信息")
    def test_search_staff_by_name(self):
        para = {"pageNum": 1, "pageSize": 10, "username": "staff"}
        ret = self.req_by_test('search_staff', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1, "pageSize": 10, "username": "testXXX"}
        ret = self.req_by_test('search_staff', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.feature("导出所有人员信息")
    def test_export_staff(self):
        for api in self.api_data:
            if api['api_name'] in "export_staff":
                ret = self.session.download_file(api['req'], api['method'], filename='staff.csv')

    @allure.feature("删除指定人员信息")
    def test_delete_staff_by_id(self):
        self.req_by_test('delete_staff', self.api_data, add_url=self.staff_id)
        para = {"pageNum": 1, "pageSize": 10, "username": "auto_test"}
        ret = self.req_by_test('search_staff', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

