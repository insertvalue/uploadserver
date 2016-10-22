#!/usr/bin/python
#encoding=utf8

import tarfile
import ConfigParser
import threading
import os
import shutil

#destroot = 'D:/ibserver_build/'
destroot = os.path.abspath('../..')+'/build/'
destdir = destroot + 'ibserver/ibserver'

filetypes = ['.py', '.conf', '.txt', '.sh']
not_build_files = ['build.py']

if os.path.exists(destroot):
    shutil.rmtree(destroot)
os.makedirs(destroot)
os.makedirs(destdir)

home = os.getcwd()

files = os.listdir(home)
for filename in files:
    newPath = os.path.join(home, filename)
    if os.path.splitext(newPath)[1] in filetypes and filename not in not_build_files and '.svn' not in newPath:
        shutil.copy(newPath, os.path.join(destdir, filename))

unzip_tar_dir = destdir.rstrip('ibserver')


f = tarfile.open(unzip_tar_dir + 'ibserver.tar.gz', 'w:gz')

cpfiles = ['ibserver.conf', 'startup.sh', 'shutdown.sh', 'README.txt']

files = os.listdir(destdir)
for filename in files:
    newPath = os.path.join(destdir, filename)
    if os.path.isdir(newPath):
        f.add(newPath, 'ibserver/' + filename)
        shutil.rmtree(newPath)
    elif os.path.isfile(newPath):
        if filename in cpfiles:
            shutil.move(newPath, os.path.join(unzip_tar_dir, filename))
        else:
            f.add(newPath, 'ibserver/' + filename)
            os.remove(newPath)
f.close()
shutil.rmtree(destdir)

destrootdir = destdir.split('ibserver/')[0]
f = tarfile.open(destrootdir + 'ibserver.tar.gz', 'w:gz')
f.add(unzip_tar_dir, 'ibserver')
f.close()
shutil.rmtree(unzip_tar_dir)
print 'build succed...'
