# coding=utf-8
# @Time    : 2019/8/4 0004 22:51
# @Author  : xiaodeme@163.com
# @FileName: img_download_single.py
# @Software: PyCharm
# @github    : https://github.com/xiaodeme
import sys
sys.path.append('../')
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import html
from utils import access_data_utils
from utils import file_utils
from utils import file_download_utils
from utils import  log_utils
import  random
import logging
import ConfigParser

# 读取配置文件
cf = ConfigParser.ConfigParser()
cf.read("../etc/base_config.cfg")
def get_img_info(url):
    """
    获取下载图集信息，
        图片数量：观察发现，图片名称是按序号生成，所以获取图片数量即可生成图片下载地址
        图片名称：生成文件夹路径，若名称解析失败，文件夹为随机数字
    :param url:
    :return:
    """
    logging.info("正在获取图集下载信息:%s" % (url))
    data = access_data_utils.access_url(url)

    # with open("F:/images/index/28539.html") as f:
    #     data = f.read()

    img_dict = {}
    selector = html.fromstring(data)
    #获取当前图集总数、名称
    #因为图集总数、名称行数不固定，故检索判断获取
    p_text_list = selector.xpath('.//div[@class="tuji"]/p')
    for p_text in p_text_list:
        p_info = p_text.xpath("text()")[0]
        if p_info.rfind("出镜模特") > -1:
            try:
                img_name = p_text.xpath("a/text()")[0]
            except BaseException, e:
                logging.error("异常信息:%s" %(e))
                img_name = str(random.randint(1, 100))
                logging.info("获取img_name错误，随机生成文件夹名称:%s" % (img_name))

            img_dict["img_name"] = img_name
        if p_info.rfind("图片数量") > -1:
            img_count = p_info[p_info.index("P") - 2:p_info.index("P")]
            img_dict["img_count"] = img_count

    logging.info("计划下载图集总数量:%s,保存图集名称:%s" % (img_dict["img_count"],img_dict["img_name"]))
    return img_dict

def img_download(root_path,img_url):

    #1. 获取下载图集信息
    img_info = get_img_info(img_url)
    img_name =  img_info["img_name"]
    img_count = int(img_info["img_count"])

    #2.创建图片保存路径
    save_folder = root_path + "/" + img_name
    file_utils.mkdir_path(save_folder)

    #3.开始图集下载
    img_type_id = img_url[img_url.rfind("a")+2:img_url.rfind("/")]
    logging.info("当前[%s]图集下载地址:%s" % (img_name,img_url))
    logging.info("当前[%s]图集下载总数img_count=%s,img_type_id=%s" % (img_name,img_count,img_type_id))

    for index in range(img_count):
        img_download_url = cf.get("base_config","img_download_url")
        img_download_url = img_download_url.format(img_type_id, index)
        # logging.info("当前图片下载地址:%s" % (img_download_url))

        file_download_utils.img_download(save_folder,img_download_url)

    logging.info("当前[%s]图集下载完成" %(img_name))

if __name__ == '__main__':
    root_path = cf.get("base_config","root_path")
    index_url = cf.get("base_config", "index_url")
    file_utils.mkdir_path(root_path)

    log_name = root_path + "/" + "log.log"
    log_utils.log_config(log_name)

    print("图集正确地址查看:%s" %(index_url))
    print("图集正确输入地址:%s"  % ("https://www.meituri.com/a/22523/"))
    href = raw_input('请输入图集下载类型：')

    print("您输入的图集地址是:%s" % (href))
    print("当前图集保存文件夹:%s " % (root_path))
    print("当前图集下载日志查看:%s " % (log_name))

    img_download(root_path,href)


    # pass