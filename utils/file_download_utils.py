# coding=utf-8
# @Time    : 2019/8/4 0004 22:48
# @Author  : xiaodeme@163.com
# @FileName: file_download_utils.py
# @Software: PyCharm
# @github    : https://github.com/xiaodeme
import urllib2
import cookielib
import time
import file_utils
import log_utils
import logging

def get_file(url):
    """
    根据指定路径下载数据(图片)
    :param url:
    :return:
    """
    try:
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        req = urllib2.Request(url)
        operate = opener.open(req)
        data = operate.read()
        logging.info("当前图片下载完成:%s" % (url))
        return data
    except BaseException, e:
        print e
        return None


def save_file(folder_path, file_name, data):
    """
    将下载图片存入指定路径
    :param folder_path:
    :param file_name:
    :param data:
    :return:
    """
    if data == None:
        return

    if (not folder_path.endswith("/")):
        folder_path = folder_path + "/"

    folder_path = file_utils.mkdir_path(folder_path)
    file = open(folder_path + file_name, "wb")
    file.write(data)
    file.flush()
    file.close()

import access_data_utils
def img_download(root_path,img_url):
    """
    根据图片地址下载到指定路径
    :param root_path:
    :param img_url:
    :return:
    """
    img_data = get_file(img_url)
    # img_data = access_data_utils.access_url(img_url)
    file_name = file_utils.unique_str() + file_utils.get_file_extension(img_url)

    save_file(root_path, file_name, img_data)


if __name__ == '__main__':

    log_name = "log.log"
    root_path = "F:/images"
    img_url = 'https://ii.hywly.com/a/1/22523/1.jpg'
    log_name = root_path + "/" + log_name
    log_utils.log_config(log_name)


    img_download(root_path,img_url)