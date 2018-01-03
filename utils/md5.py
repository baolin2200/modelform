#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2017/12/29
import hashlib


def md5(text):
    m = hashlib.md5()
    m.update(text.encode("utf-8"))
    return m.hexdigest()


if __name__ == '__main__':
    text = "baolin"
    print(md5(text))

