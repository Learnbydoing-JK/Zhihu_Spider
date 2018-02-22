#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 字符清洗部分代码于博客 http://blog.csdn.net/u012155582/article/details/78587394 的基础上修改

import re
import jieba_fast as jieba
from collections import Counter

questionId = 267189851
fileName = 'comments' + str(questionId)


def is_valid(uchar):
    """判断一个unicode字符是否是汉字或数字"""
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    elif u'\u0030' <= uchar <= u'\u0039':
        return True
    else:
        return False


def format_str(content):
    content_str = ''
    for i in content:
        if is_valid(i):
            content_str = content_str + i
        else:
            content_str = content_str + ' '
    return content_str


f1 = open(fileName + '.txt', 'r', encoding='utf-8')

formatted = ''
lines = f1.readlines()
f1.close()
for line in lines:
    formatted += format_str(line[4:]) + ' '
# print(formatted)


words = []
word_piece = jieba.cut(formatted, cut_all=False)
words.extend(word_piece)

count = Counter(words)
result = sorted(count.items(), key=lambda x: x[1], reverse=True)
# print(result)

f2 = open(fileName + '-result.txt', 'w')
for res in result:
    # print(res[0], res[1])
    res_piece = '%-8s%8s\n' % (res[0], res[1])
    f2.write(res_piece)
f2.close()
print('Done.')
