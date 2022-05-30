import time
import re
import tesserocr
from selenium import webdriver
from io import BytesIO
from PIL import Image
from retrying import retry
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import numpy as np

"""
使用Selenium自动化识别网站中的验证码
"""
def preprocess(image):
    image = image.convert('L')
    array = np.array(image)
    array = np.where(array > 50, 255, 0)
    image = Image.fromarray(array.astype('uint8'))
    return image

#设置重试次数和重试条件
@retry(stop_max_attempt_number=10, retry_on_result=lambda x: x is False)
def login():
    #打开指定网站
    browser.get('https://captcha7.scrape.center/')
    #找到输入框，并输入信息
    browser.find_element_by_css_selector('.username input[type="text"]').send_keys('admin')
    browser.find_element_by_css_selector('.password input[type="password"]').send_keys('admin')
    #案例验证码图片为Canvas绘制的
    captcha = browser.find_element_by_css_selector('#captcha')
    #截取验证码图片，转化为图片对象
    image = Image.open(BytesIO(captcha.screenshot_as_png))
    #去噪处理
    image = preprocess(image)
    captcha = tesserocr.image_to_text(image)
    #去除识别结果中的一些非字母字符和数字字符
    captcha = re.sub('[^A-Za-z0-9]', '', captcha)
    browser.find_element_by_css_selector('.captcha input[type="text"]').send_keys(captcha)
    browser.find_element_by_css_selector('.login').click()
    try:
        #等待登陆成功的字样出现，如果出现就证明验证码识别正确，否则重复以上步骤重试
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//h2[contains(., "登录成功")]')))
        time.sleep(10)
        browser.close()
        return True
    except TimeoutException:
        return False


if __name__ == '__main__':
    browser = webdriver.Chrome()
    login()
