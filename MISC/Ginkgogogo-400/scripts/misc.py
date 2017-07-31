# coding=utf-8
import os
import subprocess
import random
import md5

def md5_encode():
	password = str(random.uniform(100000,999999))[:6]
	hash_pass = md5.new()
	hash_pass.update(str(password))
	newpass = str(hash_pass.hexdigest())
	return password,newpass

def mk_file(file_name,password):
	fp = open(file_name,'w')
	fp.write(password)
	fp.close()

def del_file(get_cwd,oldpass):
	list_dir = os.listdir(get_cwd)
	if oldpass + '.zip' in list_dir:
		os.remove(oldpass + '.zip')
	if oldpass + '.txt' in list_dir:
		os.remove(oldpass + '.txt')


def create_archive(get_cwd):
	password,newpass = md5_encode()
	rc = subprocess.call(['7z', 'a', '-p%s' % password, '-y', '%s.zip' % newpass] + ['key.txt','五年计划.exe'])

	count = 499
	while count:
		password_old = password
		oldpass = newpass
		password,newpass = md5_encode()
		file_name = str(oldpass) + '.txt'
		mk_file(file_name,password_old)
		rc = subprocess.call(['7z', 'a', '-p%s' % password, '-y', '%s.zip' % newpass] + ['%s.zip' % oldpass,file_name])
		
		del_file(get_cwd,oldpass)
		count -= 1
	mk_file(file_name,password)
	
	return password

if __name__ == '__main__':
	get_cwd = os.getcwd()
	ok = create_archive(get_cwd)
	if ok:
		print ok
		print "Done."
