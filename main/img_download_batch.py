# coding=utf-8
# @Time    : 2019/8/4 0004 23:14
# @Author  : xiaodeme@163.com
# @FileName: img_download_batch.py
# @Software: PyCharm
# @github    : https://github.com/xiaodeme
import sys
sys.path.append('../')
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import html
from utils import access_data_utils
from utils import file_utils
from utils import log_utils
from main import img_download_single
import logging
import ConfigParser
# 读取配置文件
cf = ConfigParser.ConfigParser()
cf.read("../etc/base_config.cfg")





def get_img_list(url):
    """
    根据分类地址获取当前分类下的图集地址(分类 > 下载图集):目前仅下载分类首页(最多40套)，未按分类全部页码
    :param url:
    :return:
    """
    logging.info("准备开始图集下载:%s:" %(url))
    data = access_data_utils.access_url(url)
    img_list = []
    selector = html.fromstring(data)
    p_text_list = selector.xpath('.//div[@class="hezi"]/ul/li/a')
    for i in p_text_list:
        href =  i.xpath("@href")[0]
        img_list.append(href)
    return img_list



def img_download_by_img_type(root_path,index_url):
    """
     按分类下载图集
    :return:
    """

    # 1. 显示图集分类
    img_type_url_list = file_utils.show_img_type_url_list(index_url)

    # 2. 选择图集分类
    img_type = input(u'请输入图集下载类型[输入数字]：')

    text = img_type_url_list[img_type - 1]["text"]
    href = img_type_url_list[img_type - 1]["href"]
    print("您选择下载的图集是:%s,图集下载地址:%s" % (text, href))
    root_path = root_path + "/" + str(img_type)
    print("当前图集保存文件夹:%s " % (root_path))
    print("当前图集下载日志查看:%s " % (log_name))

    # 3.开始分类下载
    img_list = get_img_list(href)
    for url in img_list:
        img_download_single.img_download(root_path, url)

if __name__ == '__main__':

    root_path = cf.get("base_config", "root_path")
    file_utils.mkdir_path(root_path)

    index_url = cf.get("base_config", "index_url")
    log_name = root_path + "/" + "log.log"
    log_utils.log_config(log_name)


    img_download_by_img_type(root_path,index_url)