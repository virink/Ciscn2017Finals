#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

###############################
#							   
#			By Ginkgo		   
#			 2017.07		   
#							   
###############################

import os
import subprocess

__author__ = 'MoR03r'
__enviroment__ = 'Ubuntu 16.04'

def uncompressfile(key_name,file_name):
	try:
		key_fp = open(key_name,'r')
		key_val = key_fp.read()
		key_fp.close()
		rc = subprocess.call(['7z', 'e', '-p%s' % key_val, '-y', file_name])
		old_key_name = key_name
		old_file_name = file_name
		if old_file_name[:6] == old_key_name[:6]:
			os.remove(old_key_name)
		os.remove(old_file_name)
	except:
		exit()

def get_file():
	get_cwd = os.getcwd()
	while True:
		file_names = os.listdir(get_cwd)
		for files in file_names:
			if '.txt' in files:
				key_name = files
			elif '.zip' in files:
				if '五指山' in files:
					continue
				file_name = files
			else:
				pass
		uncompressfile(key_name,file_name)

if __name__ == '__main__':
	get_file()