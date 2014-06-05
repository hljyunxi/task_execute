#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

#点分十进制到int类型互相转换

def ip2int(ipstr):
    return int(''.join(['%02x'%int(i) for i in ipstr.split('.')]), 16)

def int2ip(ipint):
    out = []
    for i in range(4):
        ipint, n = divmod(ipint, 256)
        out.append(str(n))
    return '.'.join(out)
