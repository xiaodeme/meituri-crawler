# coding=utf-8
# @Time    : 2019/8/4 0004 22:48
# @Author  : xiaodeme@163.com
# @FileName: file_utils.py
# @Software: PyCharm
# @github    : https://github.com/xiaodeme
import os
import uuid
from lxml import html
from utils import access_data_utils
import logging

def mkdir_path(foder_path):
    # 去除左右两边的空格
    path = foder_path.strip()
    # 去除尾部 \符号
    path = path.rstrip("\\")
    if  not os.path.exists(path):
        os.makedirs(foder_path)
    return path


def unique_str():
    """
    自动生成一个唯一的字符串，固定长度为36
    :return:
    """
    return str(uuid.uuid1())

def get_file_extension(file):
    """
    获取文件后缀
    :param file:
    :return:
    """
    return os.path.splitext(file)[1]

def get_img_type_list(index_url):
    """
    根据首页信息获取所有分类下载地址
    :param index_url:首页地址
    :return:
    """
    # 这里将首页保存到了本地，可直接解析
    logging.info("正在解析首页:%s，获取图集分类地址,请稍等..." %(index_url))
    data = access_data_utils.get_html_data(index_url)
    img_list=[]
    img_list_info = {}
    index = 1
    selector = html.fromstring(data)
    for info in selector.xpath('//ul[@id="tag_ul"]/li/a'):
        href = info.xpath("@href")[0]
        text = info.xpath("text()")[0]

        img_list_info["index"] = index
        img_list_info["text"] = text
        img_list_info["href"] = href
        img_list.append(img_list_info)

        img_list_info = {}
        index += 1
    return img_list

def show_img_type_url_list(index_url):
    """
    显示图集下载分类地址
    :param index_url:
    :return:
    """
    # 1. 选择显示分类
    show_img_type_url_list = get_img_type_list(index_url)
    # print img_list
    for info in show_img_type_url_list:
        print("%s.%s==%s" % (info["index"], info["text"], info["href"]))
    return show_img_type_url_list