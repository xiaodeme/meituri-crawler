# coding=utf-8
# @Time    : 2019/8/4 0004 22:51
# @Author  : xiaodeme@163.com
# @FileName: access_data_utils.py
# @Software: PyCharm
# @github    : https://github.com/xiaodeme

import urllib2
# from selenium import webdriver

def get_html_data(url):
    html_data = urllib2.urlopen(url).read()
    return html_data

#
# def access_url(url):
#     option = webdriver.ChromeOptions()
#     option.add_argument("headless")
#     browser = webdriver.Chrome(chrome_options=option)
#     browser.get(url)  # Load page
#     # 获得网页数据
#     data = browser.page_source
#     browser.close()
#     # browser.quit()
#     return  data
