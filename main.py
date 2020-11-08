import json

import os
import random
import time
from log.logg import log_init
import logging
import key_word
from conf import site


from util import db_util
from util import request_util

logger = logging.getLogger(__file__)

"""

1.通过不同网站搜索doi
    a.通网站名获取配置
    b.通过关键搜索
    c。保存doi

2.通过doi下载bib
    a.按照每一行读取doi

3.通过doi在谷歌学术上下载pdf


"""


# step 1
def read_conf(key):
    site_list = site.site_list
    base_path = 'conf/'
    for entry in site_list.items():
        if entry[1]:
            function_name = entry[0]
            filename = os.path.join(base_path, entry[0] + '.json')
            logger.info("读文件：%s" % filename)
            with open(filename, mode='r') as f:
                conf = json.load(f)
                logger.info("执行%s search_by_key" % function_name)
                search_by_key(conf, key, function_name)

    return True


# step 2
def search_by_key(conf, key, site_type):
    doi_new = request_util.search_by_key(conf, key, site_type)
    if not doi_new:
        return
    db_util.insert_manny(doi_new)


# step 3
def download_cite_byDOI():
    """
    1.获取没有更新bib的条目
    2.请求bib
    3.更新数据库
    :return:
    """

    count, data_list = db_util.get_all_without_bib()
    logger.info("待更新bib条目：%d"%count)
    logger.info(data_list)
    for item in data_list:
        doi = item['doi']
        res = request_util.download_cite_byDOI(doi)
        t = random.randint(15, 20)  # 随机睡眠防止ip被封
        time.sleep(t)
        logger.info(res)
        if not res:
            return False
        logger.info("更新数据库")
        db_util.update_bib_one((True,res['bib'],res['title'],doi))

    return True



# step 4
def download_pdf_byDOI():
    count, data_list = db_util.get_all_without_pdf()
    logger.info("待更新pdf条目：%d" % count)
    logger.info(data_list)
    for item in data_list:
        doi = item['doi']
        title = item['title']
        res = request_util.download_pdf_byDOI_sci(doi,title)


        logger.info(res)
        if not res:
            db_util.update_fail(("未找到文章",doi))
            continue
        logger.info("更新数据库")
        db_util.update_pdf_one((True,doi))

        t = random.randint(15, 20)  # 随机睡眠防止ip被封
        time.sleep(t)

    return True




if __name__ == '__main__':
    log_init()

    # logger.info(time.time())
    # step1
    #
    # keys = key_word.key_string.split(',')
    # for key in keys:
    #     time.sleep(5)
    #     read_conf(key)

    # step2

    # download_cite_byDOI()

    # step3

    #download_pdf_byDOI()
