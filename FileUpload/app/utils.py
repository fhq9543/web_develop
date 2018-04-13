# -*- coding: utf-8 -*-
import os
import hashlib
from functools import partial

from config import UPLOAD_FOLDER

HERE = os.path.abspath(os.path.dirname(__file__))

def get_file_md5(f, chunk_size=8192):
    '''
    获得文件的md5值
    '''
    h = hashlib.md5()
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        h.update(chunk)
    return h.hexdigest()

def humanize_bytes(bytesize, precision=2):
    '''
    返回可读文件的大小
    '''
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'bytes')
    )
    if bytesize == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    return '%.*f %s' % (precision, bytesize / factor, suffix)

# 根据上传文件的目录获取文件路径
get_file_path = partial(os.path.join, HERE, UPLOAD_FOLDER)
