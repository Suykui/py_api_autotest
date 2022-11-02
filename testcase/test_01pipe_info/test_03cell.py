import sys
import os
import pytest
import yaml
import json
from utils.com_log import logger
import basecase
import allure

@allure.feature("防火分区管理")
class TestCell(basecase.BaseCase):

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

    @allure.story("查看防火分区管理界面")
    def test_get_cell(self):
        para = {"pageNum": 1, "pageSize": 10}
        ret = self.req_by_test('get_cell', self.api_data, para)
        assert ret["total"] != 0, "查询结果为空"  

    @allure.story("新增防火分区")
    def test_add_cell(self):
        para = {
            "fhfqDm": "1",
            "ggfdMc": "cell",
            "ggDm": "370050dcb35f465ea80c579fb5c1d1b41_F596293104054081956EA17A791A0D34",
            "cd": "1",
            "utid": "F596293104054081956EA17A791A0D34",
            "utConinfo": {
                "adName": "test"
            },
            "ptGg": {
                "ggMc": "test"
            },
            }
        self.req_by_test('add_cell', self.api_data, para)
        para = {"pageNum": 1, "pageSize": 10, "ggfdMc": "cell"}
        ret = self.req_by_test('search_cell', self.api_data, para)
        for i in ret['rows']:
            if i['ggfdMc']=='cell':
                TestCell.cell_id = i['id']
        assert TestCell.cell_id != None, "未获取到新增防火分区的ID，新增失败"

    @allure.story("查看指定防火分区")
    def test_view_cell_by_id(self):
        ret = self.req_by_test('view_cell', self.api_data, add_url=self.cell_id)
        assert "cell" in ret["data"]["ggfdMc"], "查询结果为空"  
    
    @allure.story("修改指定防火分区")
    def test_modify_cell_by_id(self):
        ret = self.req_by_test('view_cell', self.api_data, add_url=self.cell_id)
        data = ret['data']
        data['cd'] = 5
        ret = self.req_by_test('modify_cell', self.api_data, data)
        ret = self.req_by_test('view_cell', self.api_data, add_url=self.cell_id)
        assert ret['data']['cd'] == 5, "确认修改失败"
    
    @allure.story("搜索指定防火分区")
    def test_search_cell_by_name(self):
        para = {"pageNum": 1, "pageSize": 10, "ggfdMc": "cell"}
        ret = self.req_by_test('search_cell', self.api_data, para)
        assert len(ret['rows'] ) == 1, "搜索返回结果数目不为1"
        para = {"pageNum": 1, "pageSize": 10, "ggfdMc": "testXXX"}
        ret = self.req_by_test('search_cell', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0"

    @allure.story("导出所有防火分区")
    def test_export_cell(self):
        for api in self.api_data:
            if api['api_name'] in "export_cell":
                ret = self.session.download_file(api['req'], api['method'], filename='cell.csv')

    @allure.story("删除指定防火分区")
    def test_delete_cell_by_id(self):
        self.req_by_test('delete_cell', self.api_data, add_url=self.cell_id)
        para = {"pageNum": 1, "pageSize": 10, "ggfdMc": "cell"}
        ret = self.req_by_test('search_cell', self.api_data, para)
        assert len(ret['rows'] ) == 0, "搜索返回结果数目不为0,删除失败"    

