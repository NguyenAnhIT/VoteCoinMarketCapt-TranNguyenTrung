import os
import shutil
import tempfile
from random import randint

import undetected_chromedriver.v2 as uc
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5 import uic
from selenium import webdriver
from time import sleep
from itertools import count
import requests
import json

from selenium.webdriver import Keys


class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi('Data/Coinmarketcaps.ui',self)
        self.pushButton = self.findChild(QPushButton,'pushButton')
        self.pushButton.clicked.connect(self.start)
        self.lineEdit = self.findChild(QLineEdit,'lineEdit')
        self.lineEdit_2 = self.findChild(QLineEdit, 'lineEdit_2')
        self.lineEdit_3 = self.findChild(QLineEdit, 'lineEdit_3')
        self.spinBox = self.findChild(QSpinBox,'spinBox')
        self.label_5 = self.findChild(QLabel,'label_5')
        self.label_6 = self.findChild(QLabel,'label_6')
        self.label_7 = self.findChild(QLabel,'label_7')
        self.label_8 = self.findChild(QLabel,'label_8')
        self.checkBox = self.findChild(QCheckBox,'checkBox')
        self.checkBox_2 = self.findChild(QCheckBox,'checkBox_2')

        self.show()
        self.BoxThread = {}
        self.proxy = {}
    def start(self):
        for i in range(0,1):
            if i == 0:self.position=0
            elif i == 1:self.position=50
            elif i == 2:self.position=100
            elif i == 3:self.position=150
            self.BoxThread[i] = StartsThread(index = i)
            self.BoxThread[i].checkBox = self.checkBox
            self.BoxThread[i].checkBox_2 = self.checkBox_2
            self.BoxThread[i].position = self.position
            self.BoxThread[i].start()
            sleep(1)


class StartsThread(QThread):
    def __init__(self,index = 0):
        super(StartsThread,self).__init__()
        self.index = index
        self.is_running = True
    def run(self):
        self.handel()

    def getProxy(self):
        while True:
            proxy = requests.get(f'http://proxy.tinsoftsv.com/api/changeProxy.php?key=TL46gGJAt8IIwRhLEofwX2ZprwGYZetyeTEfH3]&location=[0]')
            proxy_data = json.loads(proxy.text)
            try:
                proxy = proxy_data['proxy']
                with open('Data/Reload/proxy.txt','w') as saveproxy:
                    saveproxy.write(proxy)
                return proxy
            except:
                with open('Data/Reload/proxy.txt','r') as openproxy:
                    openproxy = openproxy.readline()
                    if openproxy:
                        return openproxy
                    else:
                        timedelay = proxy_data['next_change']
                        while True:
                            sleep(1)
                            timedelay -= 1
                            print(timedelay)
                            if timedelay < 1:
                                break

    def setBrowser(self):
        self.temp = os.path.normpath(tempfile.mkdtemp())
        if self.checkBox.isChecked():
            proxy = self.getProxy()
            opts = webdriver.ChromeOptions()
            args = ["hide_console", ]
            opts.add_argument('--proxy-server=%s' % proxy)
            opts.add_argument("--window-size=920,880")
            opts.add_argument("--disable-popup-blocking")
            #opts.add_argument(f"--window-position={self.position},0")
            opts.add_argument("--incognito")
            #opts.add_argument('--user-data-dir=' + self.temp)
            self.browser = webdriver.Chrome(executable_path=os.getcwd()+'/chromedriver',options=opts, service_args=args)
            with self.browser: self.browser.get('https://google.com')
        if not self.checkBox.isChecked():
            opts = webdriver.ChromeOptions()
            args = ["hide_console", ]
            opts.add_argument("--window-size=920,880")
            opts.add_argument("--disable-popup-blocking")
            #opts.add_argument(f"--window-position={self.position},0")
            opts.add_argument("--incognito")
            #opts.add_argument('--user-data-dir=' + self.temp)
            self.browser = webdriver.Chrome(executable_path=os.getcwd()+'/chromedriver',options=opts, service_args=args)
            with self.browser: self.browser.get('https://google.com')
    def handel(self):
        self.setBrowser()
        sleep(5)
        self.browser.find_element_by_css_selector('.gLFyf.gsfi').send_keys('coinmarketcap braintrust')
        sleep(0.5)
        self.browser.find_element_by_css_selector('.gLFyf.gsfi').send_keys(Keys.ENTER)
        sleep(3)
        # Click web đầu tiên
        self.browser.find_element_by_css_selector('.yuRUbf').click()
        sleep(3)
        # Sử lý trình scroll
        for i in range(0, 8):
            scrollY = randint(0, 1500)
            self.browser.execute_script(f"window.scrollTo(0, {scrollY})")
            sleep(0.8)
        sleep(1)
        # Scroll Về Đầu Tiên
        self.browser.execute_script("window.scrollTo(0, 0)")
        sleep(1.5)
        # Click Về Trang Chủ
        self.browser.find_elements_by_css_selector('.cmc-link')[0].click()
        sleep(3)
        # Sử lý scroll
        for i in range(0, 8):
            scrollY = randint(0, 500)
            self.browser.execute_script(f"window.scrollTo(0, {scrollY})")
            sleep(0.8)
        # Click More
        self.browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[3]/div[1]/div[1]/a').click()
        sleep(3)
        # Sử lý scroll
        for i in range(0, 5):
            scrollY = randint(0, 550)
            self.browser.execute_script(f"window.scrollTo(0, {scrollY})")
            sleep(0.8)
        # Click random coin
        self.browser.find_elements_by_css_selector('.coin-logo')[randint(0, 15)].click()
        # Sử lý scroll
        for i in range(0, 5):
            scrollY = randint(0, 550)
            self.browser.execute_script(f"window.scrollTo(0, {scrollY})")
            sleep(0.8)
        self.browser.execute_script("window.scrollTo(0, 0)")
        sleep(1)
        # Click Search
        try:
            self.browser.find_element_by_css_selector('.sc-16r8icm-0.jZwKai').click()
        except:
            self.browser.find_element_by_css_selector('.sc-266vnq-1.gffsPR').click()
        sleep(1.5)
        # Input Keyword
        self.browser.find_element_by_css_selector('.bzyaeu-3.jUraic').send_keys('braintrust')
        sleep(1)
        # Click Select Coint
        self.browser.find_element_by_css_selector('.vcaol5-0.fnjmWk').click()
        sleep(3)
        # Click Random
        self.browser.execute_script("window.scrollTo(0, 300)")
        for i in range(1, 5):
            self.browser.find_element_by_xpath(
                f'//*[@id="__next"]/div/div/div[2]/div/div[2]/div/span/a[{randint(2, 10)}]').click()
            sleep(randint(3, 6))
        self.browser.find_element_by_xpath('//*[@id="__next"]/div/div/div[2]/div/div[2]/div/span/a[1]').click()
        # Sử lý scroll
        sleep(3)
        for i in range(0, 10):
            scrollY = randint(0, 2550)
            self.browser.execute_script(f"window.scrollTo(0, {scrollY})")
            sleep(0.8)
        self.browser.execute_script("window.scrollTo(0, 2500)")
        self.browser.execute_script("window.scrollTo(0, 2800)")
        sleep(1.5)
        # Click Show More
        self.browser.find_element_by_xpath(
            '//*[@id="__next"]/div/div/div[2]/div/div[3]/div[1]/div[2]/div[4]/button/a').click()
        # Sử lý scroll
        for i in range(0, 3):
            scrollY = randint(0, 1000)
            self.browser.execute_script(f"window.scrollTo(0, {scrollY})")
            sleep(1.5)

        sleep(5000)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    UiWindow = UI()
    app.exec()