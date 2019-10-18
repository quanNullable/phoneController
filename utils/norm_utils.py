#!/usr/bin/env python  
# encoding: utf-8  
from datetime import datetime, timedelta
import time


def current_time():
    """
    当前时间
    :return:
    """
    return datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
