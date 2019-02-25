#!python
# coding: gbk
#------------------------------
# tests.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
import os
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


# 等待服务器响应时间(10秒)
# 10秒足以捕获潜在的问题和不可预知的缓慢因素
MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
  
    def setUp(self):
        self.vBrowser = webdriver.Firefox()
        vStagingServer = os.getenv('STAGING_SERVER')
        if vStagingServer:
            self.live_server_url = 'http://{}'.format(vStagingServer)
  
    def tearDown(self):
        self.vBrowser.quit()

    def waitForRowInListTable(self, vRowText):
        vStartTime = time.time()
        while True:
            try:
                vTable = self.vBrowser.find_element_by_id('id_list_table')
                vRows = vTable.find_elements_by_tag_name('tr')
                self.assertIn(vRowText, [ vRow.text for vRow in vRows ])
                break
            
            except (AssertionError, WebDriverException) as e:
                if ((time.time() - vStartTime) > MAX_WAIT): raise e
                time.sleep(1)


    def test_CanStartAListAndRetrieveItLater(self):
        # 访问应用首页
        self.vBrowser.get(self.live_server_url)
        
        # 页面的标题和开头都包含 "To-Do" 这个词
        self.assertIn('待办事项', self.vBrowser.title)
        self.assertIn('待办事项', self.vBrowser.find_element_by_tag_name('h1').text)
        
        # 页面有一个待办事项文本输入框
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        self.assertEqual(vInputBox.get_attribute('placeholder'), '试试输入一个待办事项吧')
        
        
        # 输入第一个待办事项
        vInputBox.send_keys('买一些孔雀羽毛')
        vInputBox.send_keys(Keys.ENTER)
        
        # 查看刚刚输入的待办事项
        self.waitForRowInListTable('1: 买一些孔雀羽毛')
        

        # 输入第二个待办事项
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        vInputBox.send_keys('用孔雀羽毛做假蝇')
        vInputBox.send_keys(Keys.ENTER)
        
        # 再次查看刚刚输入的待办事项
        self.waitForRowInListTable('1: 买一些孔雀羽毛')
        self.waitForRowInListTable('2: 用孔雀羽毛做假蝇')

        # 操作完毕


    def test_MultipleUsersCanStartListsAtDifferentUrls(self):
        # 用户A新建了一个待办事项
        self.vBrowser.get(self.live_server_url)
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        vInputBox.send_keys('买一些孔雀羽毛')
        vInputBox.send_keys(Keys.ENTER)
        self.waitForRowInListTable('1: 买一些孔雀羽毛')
        
        #　这时，用户A有自己唯一的URL
        vUserAUrl = self.vBrowser.current_url
        self.assertRegex(vUserAUrl, '/lists/.+/')
        
        # 用户A关闭了会话
        self.vBrowser.quit()
        
        # 用户B开启了一个新会话
        self.vBrowser = webdriver.Firefox()
        
        # 用户B开始访问清单首页
        # 页面中看不到用户A的清单
        self.vBrowser.get(self.live_server_url)
        vPageText = self.vBrowser.find_element_by_tag_name('body').text
        self.assertNotIn('买一些孔雀羽毛', vPageText)
        self.assertNotIn('做假蝇', vPageText)
        
        # 用户B新建了一个待办事项
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        vInputBox.send_keys('买一盒牛奶')
        vInputBox.send_keys(Keys.ENTER)
        self.waitForRowInListTable('1: 买一盒牛奶')
        
        # 用户B获得了自己唯一的URL
        vUserBUrl = self.vBrowser.current_url
        self.assertRegex(vUserBUrl, '/lists/.+/')
        self.assertNotEqual(vUserAUrl, vUserBUrl)
        
        # 用户B看不到用户A的清单
        # 只能看到自己的清单
        vPageText = self.vBrowser.find_element_by_tag_name('body').text
        self.assertNotIn('买一些孔雀羽毛', vPageText)
        self.assertIn('买一盒牛奶', vPageText)

        # 操作完毕


    def test_LayoutAndStyling(self):
        # 访问应用首页
        self.vBrowser.get(self.live_server_url)
        self.vBrowser.set_window_size(1024, 768)
        
        # 输入框居中显示
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        self.assertAlmostEqual( \
            vInputBox.location['x'] + vInputBox.size['width'] / 2, \
            512, \
            delta=10 \
        )
        
        vInputBox.send_keys('testing')
        vInputBox.send_keys(Keys.ENTER)
        self.waitForRowInListTable('1: testing')
        
        # 输入框居中显示
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        self.assertAlmostEqual( \
            vInputBox.location['x'] + vInputBox.size['width'] / 2, \
            512, \
            delta=10 \
        )

