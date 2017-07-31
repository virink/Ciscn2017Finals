#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

###############################
#							   
#			By Ginkgo		   
#			 2017.07		   
#							   
###############################

# 题目简单，没写解密脚本
# 压缩包密码是数字和字符,爆破能得到7@.7@!2

import md5
import random

__author__ = 'MoR03r'
__enviroment__ = 'Ubuntu 16.04'


file_wirte = open('misc.txt','ab+')
md5_hash = md5.new()
md5_hash.update("Ginkgogogo")
flag = 'flag{' + str(md5_hash.hexdigest()[8:-8]) + '}'
print flag
bin_string = ''
for i in flag:
	tmp = bin(ord(i))[2:]
	if len(tmp) < 8:
		for j in range(8-len(tmp)):
			tmp = '0' + tmp
	bin_string += tmp

manche = ''
for s in bin_string:
	if s == '0':
		manche += '10'
	else:
		manche += '01'
encode_str = ''
for v in range(0,len(manche)/4):
	dd = manche[4*v:4*v+4]
	if dd == '0101':
		encode_str += 'A'
	elif dd == '0110':
		encode_str += 'C'
	elif dd == '1010':
		encode_str += 'T'
	elif dd == '1001':
		encode_str += 'G'
	else:
		print "error"

pick_str = ''
for ss in encode_str:
	if ss == 'A':
		pick_str += 'T'
	elif ss == 'T':
		pick_str += 'A'
	elif ss == 'C':
		pick_str += 'G'
	else:
		pick_str += 'C'
print encode_str + '\n' + pick_str

