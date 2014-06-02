#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

import array, binascii
import impl

def default(value, function):
    if values is None:
        return function()

    return value

def int2hex(value):
    return binascii.b2a_hex(buffer(array.array('l', (value,)))) #4 bytes

def hex2int(value):
    bin = binascii.a2b_hex(value)
    index, sum = 0, 0
    for c in bin:
        sum += ord(c)<<index
        index += 8
    return sum

def import_plugins(plugin_dir):
    results = {}
    for path in glob.glob(os.path.join(plugin_dir, '*.py')):
        name, ext = name, ext = os.path.splitext(os.path.basename(path))
        if not name.startswith('_'):
            modules[name] = impl.load_source(name, path)
    return results
