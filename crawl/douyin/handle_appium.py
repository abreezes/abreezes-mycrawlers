import multiprocessing
import time

from appium import webdriver

from selenium.webdriver.support.ui import WebDriverWait


def  handle_appium(device,port):

    # cap = {
    #     "platformName": "Android",
    #     "platformVersion": "5.1.1",
    #     "deviceName": "127.0.0.1:62025",
    #     "appPackage": "com.ss.android.ugc.aweme",
    #     "appActivity": ".main.MainActivity",
    #     "noReset": "True",
    #     "unicodekeyboard": True,  # 使用输入法
    #     "resetkeyboard": True,  # 还原输入法
    # }
    """多任务端抓取"""
    cap = {
        "platformName": "Android",
        "platformVersion": "7.1.2",
        "deviceName": device,
        'udid':device,
        "appPackage": "com.baidu.searchbox",
        "appActivity": "com.baidu.searchbox.SplashActivity",
        "noReset": "True",
        "unicodekeyboard": True,  # 使用输入法
        "resetkeyboard": True,  # 还原输入法
    }

    driver = webdriver.Remote('http://localhost:{}/wd/hub'.format(port), cap)
    webdriverwait = WebDriverWait(driver, 30)
    try:
        accpt=webdriverwait.until(lambda x:x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/s3']"))
        if accpt:
            time.sleep(1)
            accpt.click()
    except Exception:
        pass
    try:
        id=webdriverwait.until(lambda x:x.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.ss.android.ugc.aweme:id/am1']"))
        if id:
            time.sleep(1)
            id.click()
    except:
        pass

    handle(driver,webdriverwait)
#


def get_size(driver):
    x=driver.get_window_size()['width']
    y=driver.get_window_size()['height']
    return (x,y)

def handle(driver,webdriverwait):
    try:
        key=webdriverwait.until(lambda x:x.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/acx']"))
        if key:
            time.sleep(1)
            key.click()
            time.sleep(1)
            key.send_keys('191433445')
            while key.text != '191433445':
                key.send_keys('191433445')
                time.sleep(0.5)
    except:
        pass
    try:
        search=webdriverwait.until(lambda x:x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/ad0']"))
        if search:
            time.sleep(1)
            search.click()
    except:
        pass

    try:
        usertag=webdriverwait.until(lambda x:x.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[3]/android.widget.LinearLayout/android.widget.TextView"))
        if usertag:
            time.sleep(1)
            usertag.click()
            webdriverwait.until(lambda x: x.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[3]/android.widget.LinearLayout/android.widget.TextView")).driver.tap((277,118),(323,150))
    except:
        pass

    try:
        user=webdriverwait.until(lambda x:x.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.View/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]"))
        if user:
            time.sleep(1)
            user.click()
    except:
        pass
    fans=webdriverwait.until(lambda x:x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/aev']"))
    if fans:
        fans.click()

    l = get_size(driver)
    x1 = int(l[0]*0.5)
    y1 = int(l[1]*0.75)
    y2 = int(l[1]*0.25)
    while True:
        if '没有更多了' in driver.page_source:
            break
        driver.swipe(x1,y1,x1,y2)
        time.sleep(0.5)

if __name__ == '__main__':
    # 多任务进行appium抓取
    m_list=[]
    devices_list=['127.0.0.1:62001','127.0.0.1:62025']

    for device in range(len(devices_list)):
        port = 4723 + 2 * device
        m_list.append(multiprocessing.Process(target=handle_appium(devices_list[device],port,)))

    for m1 in m_list:
        m1.start()

    for m1 in m_list:
        m1.join()
    # 单任务
    # driver=webdriver.Remote('http://localhost:4723/wd/hub',cap)
    # webdriverwait=WebDriverWait(driver,30)