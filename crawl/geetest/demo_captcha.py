import time
from io import BytesIO
import random

from PIL import Image

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir
from os.path import abspath, dirname
from operator import itemgetter


TEMPLATES_FOLDER = dirname(abspath(__file__)) + '/templates/'


class WeiboCookies():
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path=r'C:\Python36\chromedriver.exe')
        self.wait = WebDriverWait(self.browser, 20)
        self.BORDER = 6



    def go_security(self):
        """安全验证"""
        geetest = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_radar_tip_content')))
        if geetest:
            geetest.click()
            time.sleep(2)
            return True
        else:
            return False

    def get_bg_image(self):
        """获取完整/缺口背景图片"""

        if self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_slice'))):

            # 隐藏滑块
            self.browser.execute_script('document.querySelector(".geetest_canvas_slice").style.display = "None"')
            # 获取缺口图片

            # self.get_screenshot('./gap_bg.png','/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div/a/div[1]/div/canvas[1]')
            self.get_screenshot('./gap_bg.png','/html/body/div[3]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[1]')

            # 获取完整背景图片
            self.browser.execute_script('document.querySelector(".geetest_canvas_fullbg").style.display = "block"')
            self.get_screenshot('./full_bg.png','/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div/a/div[1]/canvas')


            # 还原状态
            self.browser.execute_script('document.querySelector(".geetest_canvas_slice").style.display = "block"')
            self.browser.execute_script('document.querySelector(".geetest_canvas_fullbg").style.display = "None"')
            return True
        else:
            return False

    def get_gap(self):
        """
        获取缺口偏移量
        :param img1: 不带缺口图片
        :param img2: 带缺口图片
        :return:
        """

        offset = -1
        #阀值
        threshold=50
        import cv2
        img1 = cv2.imread('./gap_bg.png')
        img2 = cv2.imread('./full_bg.png')

        #匹配函数如下（注意 imread 函数读到的像素值是 uint8 类型，相减之后可能溢出，所以要转为 int）
        def match(i1, i2, t):
            p1 = [int(p) for p in i1]
            p2 = [int(p) for p in i2]
            if abs(p1[0] - p2[0]) < t and abs(p1[1] - p2[1]) < t and abs(p1[2] - p2[2]) < t:
                return True
            return False
        #对两张图片逐个像素进行匹配，如果某个像素点不匹配，该像素点就是滑块缺口的左上顶点。
        # 滑块的位移是水平方向的，初始滑块左上顶底横坐标大约是 12，所以 offset = j - 12
        for j in range(260):
            for i in range(160):
                if not match(img1[i][j], img2[i][j], threshold):
                    offset = j
                    return offset
        return offset



    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        distance += 20  # 先滑过一点，最后再反着滑动回来

        # 移动轨迹
        forward_tracks = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 3 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            forward_tracks.append(round(move))
        # 反着滑动到准确位置
        back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]  # 总共等于-20

        return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}
        # return track

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        while True:
            try:
                slider = self.browser.find_element_by_xpath("//div[@class='geetest_slider_button']")
                break
            except:
                time.sleep(0.5)
        return slider

    def move_to_gap(self, slider, tracks):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        # button = self.browser.find_element_by_class_name('geetest_slider_button')
        ActionChains(self.browser).click_and_hold(slider).perform()

        # 匀速滑动
        for track in tracks['forward_tracks']:
            ActionChains(self.browser).move_by_offset(xoffset=track, yoffset=0).perform()

            # 反向滑动
        time.sleep(0.3)
        for back_track in tracks['back_tracks']:
            ActionChains(self.browser).move_by_offset(xoffset=back_track, yoffset=0).perform()

            # 小范围震荡一下，进一步迷惑极验后台，这一步可以极大地提高成功率
        ActionChains(self.browser).move_by_offset(xoffset=-3, yoffset=0).perform()
        ActionChains(self.browser).move_by_offset(xoffset=3, yoffset=0).perform()

        # 成功后，骚包人类总喜欢默默地欣赏一下自己拼图的成果，然后恋恋不舍地松开那只脏手
        time.sleep(0.3)
        ActionChains(self.browser).release().perform()


    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        self.browser.get('https://www.geetest.com/Sensebot/')

        # 安全验证
        if self.go_security():

            # 如果没有极验验证
            # 获取背景图片
            if self.get_bg_image():
                # 获取缺口位置
                gap = self.get_gap()
                print('缺口位置', gap)

                # 获取偏移量
                track = self.get_track(gap- self.BORDER)

                # 点按呼出缺口
                slider = self.get_slider()
                # 拖动滑块到缺口处
                self.move_to_gap(slider, track)
                try:
                    return bool(
                        WebDriverWait(self.browser, 5).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'lite-iconf-profile'))))
                except TimeoutException:
                    return False

            else:
                try:
                    return bool(
                        WebDriverWait(self.browser, 5).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'lite-iconf-profile'))))
                except TimeoutException:
                    return False
        else:
            try:
                return bool(
                    WebDriverWait(self.browser, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'lite-iconf-profile'))))
            except TimeoutException:
                return False

    # def do_crack(browser, offset):
    #     knob = browser.find_element_by_class_name("geetest_slider_button")
    #     fake_drag(browser, knob, offset)
    #     return

    def get_position(self,code_element):
        """获取验证码位置"""
        left = code_element.location['x']
        top = code_element.location['y']
        right = code_element.location['x'] + code_element.size['width']
        bottom = code_element.location['y'] + code_element.size['height']

        return left,top,right,bottom

    def get_screenshot(self,filename,name):
        """截取验证码范围"""
        code_element = self.wait.until(EC.presence_of_element_located((By.XPATH, name)))
        self.browser.get_screenshot_as_file('./allscreenshot.png')
        left, top, right, bottom=self.get_position(code_element)

        im = Image.open('./allscreenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save(filename)
        return im


    def main(self):
        """
        破解入口
        :return:
        """

        # 如果不需要验证码直接登录成功
        if self.login_successfully():
            # cookies = self.get_cookies()

            return {
                'status': 1,
            }



if __name__ == '__main__':
    result = WeiboCookies().main()
    print(result)
