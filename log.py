# @Time : 2021/7/6 5:40 下午
# @Author : Bais
# @Email : 17343001493@163.com
# @File : log.py

import logging
import os
log_path = os.path.join(os.path.dirname(__file__), "log/")
print(os.path.dirname(__file__))
print(log_path)
# 创建一个logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# 创建一个handler，用于写入日志文件
# log_path = os.path.dirname(__file__)+ "/log/"  # 指定文件输出路径，注意logs是个文件夹，一定要加上/，不然会导致输出路径错误，把logs变成文件名的一部分了
# print(log_path)
logname = log_path + 'out.log'  # 指定输出的日志文件名
fh = logging.FileHandler(logname, encoding='utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
fh.setLevel(logging.DEBUG)  # 设置日志器将会处理的日志消息的最低严重级别，设置为DEBUG
# 创建一个handler，用于将日志输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)
if __name__ == '__main__':
    logger.debug("User %s is loging" % 'admin')
