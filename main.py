#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 程序入口文件

from init import *

# 调用http控制器
hc = C('http')()
hc.start()

host = hc.conf['host'] if hc.conf['host'] else '127.0.0.1'
print('HTTPServer is running at %s:%s' % (host, hc.conf['port']))