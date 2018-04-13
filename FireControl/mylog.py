"""
logging配置
"""

import os
import logging.config

# 定义日志输出格式 结束

file_dir = os.path.dirname(os.path.abspath(__file__))  # log文件的目录
BASE_LOG_DIR = os.path.join(file_dir, 'log')

PREFIX_LOG = 'xiaofang'
default_log = PREFIX_LOG + '_info.log'
error_log = PREFIX_LOG + '_error.log'

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(BASE_LOG_DIR):
    os.mkdir(BASE_LOG_DIR)

# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format':'[%(levelname)s][%(asctime)s][task_id:%(name)s][%(filename)s:%(lineno)d] : %(message)s',
            'datefmt':'%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format':'[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] : %(message)s',
            'datefmt':'%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {},
    'handlers': {
        #打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        #打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'filename': os.path.join(BASE_LOG_DIR, default_log),  # 日志文件
            'formatter': 'standard',
            'maxBytes': 1024*1024*5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        #打印到文件的日志:收集错误及以上的日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, error_log),  # 日志文件
            'formatter': 'standard',
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',
        },

    },
    'loggers': {
        #logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['default', 'console', 'error'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}

logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置
logger = logging.getLogger(__name__)  # 生成一个log实例
