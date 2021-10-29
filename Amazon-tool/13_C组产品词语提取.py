# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 19:17:31 2019

@author: Administrator
"""

import jieba
import jieba.analyse
import re
import numpy as np
import pandas as pd

#打开文件路径
file = open(r"C:\Users\Administrator\Desktop\分词\Czu-FBA-utf-8.txt",'r',encoding = 'utf-8').read()
#手动增加关键词
jieba.add_word('圣诞')
jieba.add_word('情趣')
jieba.add_word('护理')

#调用停用词,设置停用词表
def stop_word():
    file = open(r"E:\02学习资料\python\stop_word-utf-8.txt",'r',encoding = 'utf-8').read()
    stop_list = list(file.split('\n'))
    return stop_list

stop_words = stop_word()

#对文本进行切割
words = jieba.lcut(file,cut_all = True)

#对文本进行统计分析
counts = {}
for word in words:
    if word in stop_words:
        continue
    elif len(word) == 1:
        continue
    elif word == '':
        continue
    else:
        counts[word] = counts.get(word,0) + 1


counts_copy = counts.copy()

#利用正则表达式删除非中文文本格式
pattern = re.compile(r'[0-9A-Za-z]+')

for key in list(counts_copy.keys()):
    if re.search(pattern,key):
        counts_copy.pop(key)
        

#删除出现频次小于10的文本词语
for key in list(counts_copy.keys()):
    if counts_copy[key] < 10:
        counts_copy.pop(key)        


list_txt = list(counts_copy.keys())

#去除list中的非名词
f_str = []
for each in list_txt:
    f_str.append(jieba.analyse.extract_tags(each,allowPOS=('n','nr','ns')))

#将结果写入txt文件中
f_file = open(r"C:\Users\Administrator\Desktop\分词\Czu.txt",'w')
for each in f_str:
    if ''.join(each) != '':
        f_file.write(''.join(each) + '\t' + str(100) + '\n')

f_file.close()






















