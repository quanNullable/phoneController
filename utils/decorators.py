#!/usr/bin/env python  
# encoding: utf-8  
import time

# 计算时间函数
def print_run_time(func):
    def wrapper(*args, **kw):
        local_time = time.time()
        func(*args, **kw)
        print('current Function [%s] run time is %.2f' % (func.__name__, time.time() - local_time))
