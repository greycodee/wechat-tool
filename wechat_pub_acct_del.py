import time

from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class WeChatPubAcct:
    driver = None

    def __init__(self, appium_config=None):
        if appium_config is None:
            raise RuntimeError('appium_config 不能为空')
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', appium_config)

    def open_wechat_pub_acct_list(self):
        # 点击通讯录
        txl_xpath = '//android.widget.FrameLayout[@content-desc="当前所在页面,与的聊天"]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]'
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath(txl_xpath))
        el = self.driver.find_element_by_xpath(txl_xpath)
        el.click()

        # 点击公众号
        gzh_xpath = '//android.widget.FrameLayout[@content-desc="当前所在页面,与的聊天"]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/com.tencent.mm.ui.mogic.WxViewPager/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.RelativeLayout[5]/android.widget.LinearLayout'
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath(gzh_xpath))
        gzh = self.driver.find_element_by_xpath(gzh_xpath)
        gzh.click()

    def get_phone_size(self):
        """获取手机屏幕的大小"""
        width = self.driver.get_window_size()['width']

        # 获取手机屏幕的宽
        height = self.driver.get_window_size()['height']
        # 获取手机屏幕的高
        return width, height

    def swipe_up(self, duration=2000):
        """上滑操作"""
        width, height = self.get_phone_size()
        start_x, start_y = 1 / 2 * width, 3 / 4 * height
        end_x, end_y = 1 / 2 * width, 1 / 4 * height
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def get_curr_page_gzh_name(self):
        names_id = 'com.tencent.mm:id/ac5'
        WebDriverWait(self.driver, 10).until(lambda x: x.find_elements_by_id(names_id))
        names = self.driver.find_elements_by_id(names_id)
        names_set = set()
        for n in names:
            names_set.add(n.text)
        return names_set

    def delete_item(self, delete_name_list):
        self.open_wechat_pub_acct_list()
        while True:
            # TODO 改成无限循环执行交集数据，当交集为空，滑动屏幕
            while True:
                curr_page_pub_acct_list = self.get_curr_page_gzh_name()
                mix_data = curr_page_pub_acct_list & delete_name_list
                if len(mix_data) == 0:
                    break
                for n in mix_data:
                    print('正在删除公众号：' + n)
                    # delete_name_list.remove(n)
                    names_id = 'com.tencent.mm:id/ac5'
                    WebDriverWait(self.driver, 10).until(lambda x: x.find_elements_by_id(names_id))
                    item = self.driver.find_elements_by_xpath("//android.widget.TextView[@text='" + n + "']/../../../..")
                    item[0].click()

                    # time.sleep(2)
                    sett_id = '设置'
                    WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_accessibility_id(sett_id))
                    sett = self.driver.find_element_by_accessibility_id(sett_id)
                    sett.click()

                    # time.sleep(2)
                    more_id = 'com.tencent.mm:id/by8'
                    WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id(more_id))
                    more = self.driver.find_element_by_id(more_id)
                    more.click()

                    # time.sleep(2)
                    delete_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[5]'
                    WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath(delete_xpath))
                    delete = self.driver.find_element_by_xpath(delete_xpath)
                    delete.click()

                    # time.sleep(2)
                    del2_id = 'com.tencent.mm:id/ffp'
                    WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id(del2_id))
                    del2 = self.driver.find_element_by_id(del2_id)
                    del2.click()

            # if len(delete_name_list) == 0:
            #     print("删除完毕")
            #     break

            btm = self.driver.find_elements_by_id('com.tencent.mm:id/bgc')
            if not btm:
                self.swipe_up()
            else:
                break

    def get_all_gzh_acct_name(self):
        self.open_wechat_pub_acct_list()
        names_set = set()
        while True:
            names_set.update(self.get_curr_page_gzh_name())

            btm = self.driver.find_elements_by_id('com.tencent.mm:id/bgc')
            if not btm:
                self.swipe_up()
            else:
                break
        return names_set

    def quit(self):
        self.driver.quit()
