from wechat_pub_acct_del import WeChatPubAcct

delete_name_list = {'CoCo都可', '澳克士牛排汉堡'}


def config():
    return {
        "platformName": "Android",
        "platformVersion": "11",
        "deviceName": "Mi_10",
        "appPackage": "com.tencent.mm",
        "appActivity": "com.tencent.mm.ui.LauncherUI",
        "resetKeyboard": True,
        "noReset": True
    }


if __name__ == '__main__':

    cnf = config()
    print(cnf)
    wechat = WeChatPubAcct(appium_config=cnf)

    # 获取关注的所有公众号名称
    # names = wechat.get_all_gzh_acct_name()
    # print(names)

    del_list = {
        '男装分销联盟168'
    }

    wechat.delete_item(del_list)
    wechat.quit()
