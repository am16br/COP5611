#!/usr/bin/python
# -*- coding: utf-8 -*-
filecount = 300000
filesize = 1024

import random, time
from os import system
import matplotlib.pyplot as plt
import numpy as np

flush = "sudo su -c 'sync ; echo 3 > /proc/sys/vm/drop_caches'"
randfile = open("/dev/urandom", "r")

def mk_dir(args):
    print("make directory: ", )
    system("rm -rf test && mkdir test")
def rm(args):
    print("delete files: ")
    system("rm -rf test")

def read_sequential(args):
    print("read sequential: ")
    outfile = open("/dev/null", "w")
    for i in range(int(args[0] / 10)):
        infile = open("test/" + unicode(i), "r")
        outfile.write(infile.read());
def read_random(args):
    print("read random: ")
    outfile = open("/dev/null", "w")
    for i in range(int(args[0] / 10)):
        infile = open("test/" + unicode(int(random.random() * args[0])), "r")
        outfile.write(infile.read());

def write_sequential(args):
    print("write sequential: ")
    for i in range(args[0]):
        rand = randfile.read(int(args[1] * 0.5 + args[1] * random.random()))
        outfile = open("test/" + unicode(i), "w")
        outfile.write(rand)
def write_random(args):
    print("write random: ")
    for i in range(int(args[0] / 10)):
        rand = randfile.read(int(args[1] * 0.5 + args[1] * random.random()))
        outfile = open("test/" + unicode(int(random.random() * args[0])), "w")
        outfile.write(rand)

def timer(test, args):
    starttime = time.time()
    test(args)
    starttime = time.time() - starttime
    system(flush)
    return(starttime)

def graphFiles(func, filecount, filesize):
    x=[]
    y=[]
    for i in range(int(filecount / 10)):
        x.append(i)
        y.append(timer(func, (i, filesize)))
    plt.title('Variable Number of Files')
    plt.xlabel('File Count')
    plt.ylabel('Time (s)')
    plt.plot(np.array(x), np.array(y))
    plt.show()
def graphSizes(func, filecount, filesize):
    x,y=[],[]
    for i in range(int(filesize / 10)):
        x.append(i)
        y.append(timer(func, (filecount, i)))
    plt.title('Variable File Sizes')
    plt.xlabel('File Sizes (B)')
    plt.ylabel('Time (s)')
    plt.plot(np.array(x), np.array(y))
    plt.show()

def graph(x, y, xlabel, ylabel, title):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #can loop to add different lines: y1, y2,...yn
    plt.plot(np.array(x), np.array(y))
    plt.show()

def usagePattern(args):
    print("Usage Pattern:")
    #can also introduce random choice on probability for likelihood of access
    for i in xrange(len(args[0])):
        args[0][i]((int(args[2]*args[1][i]), args[3]))
        print(str(args[1][i]*100)+"%")


print("future run from cmd line: python benchmark.py <FSkernels?> <fileCount> <fileSize> <test(s)>")
#check for cmd line args
menu = {}
menu['1']="Change number of files: "+str(filecount)+" files"
menu['2']="Change file size: "+str(filesize)+" bytes"
menu['3']="Choose file systems to test"
menu['4']="Standard Test"
menu['5']="Test distribution"
menu['6']="Plot"
menu['7']="Exit"

print("Welcome to the File System Benchmarking Software")
options=[write_sequential, write_random, read_random, read_sequential]
distribution=[0.25, 0.25, 0.20, 0.29]
while True:
    options=menu.keys()
    options.sort()
    print("***** MENU *****")
    for entry in options:
        print(str(entry)+": "+str(menu[entry]))
    selection=raw_input("> ")
    if selection =='1':
        filecount = int(input("Enter number of files: "))
        menu['1']="Change number of files: "+str(filecount)+" files"
    elif selection == '2':
        filesize = int(input("Enter size of files: "))
        menu['2']="Change file size: "+str(filesize)+" bytes"
    elif selection == '3':
        print("submenu for them to mount new FS or choose from list")
        print("FFS, LFS, VFS, Ext-2/4, Resier, user defined")
        tests = int(input("from sh import mount \n mount('/dev/', '/mnt/test', '-t ext4')"))
    elif selection == '4':
        args=(filecount, filesize)
        print(timer(mk_dir, args))
        print(timer(write_sequential, args))
        print(timer(write_random, args))
        print(timer(read_sequential, args))
        print(timer(read_random, args))
        #other disk usage statistics (du command or something similar)
        print(timer(rm, args))
    elif selection == '5':  #let user choose test, and statistics of system usage
        x=0
        while(x!=4 and sum(distribution)!=1.0):
            for i in xrange(len(options)):
                print(str(i)+": "+str(options[i])+": "+str(distribution[i])+"%")
            x=int(input("Enter key to modify usage percent, or 4 to run test: "))
            if(x>=0 and x<4):
                distribution[x]=float(input("Enter as percent (ex. 0.25 or 0.5): "))
            if(sum(distribution)!=1.0):
                print("Error: does not equal 100%")
                print("Currently: "+ str(sum(distribution)))
        args=(options, distribution, filecount, filesize)
        print(timer(mk_dir, args))
        print(timer(usagePattern, args))
        print(timer(rm, args))
    elif selection == '6':
        foo = int(input("1: Test variable file counts\n2: Test variable file sizes\n> "))
        args=(filecount, filesize)
        print(timer(mk_dir, args))
        print(timer(write_sequential, args))    #write first
        if(foo==1):
            graphFiles(read_random, filecount, filesize)
        elif(foo==2):
            graphSizes(read_sequential, filecount, filesize)
        print(timer(rm, args))
    elif selection == '7':
      break
    else:
      print("Unknown Option Selected!")





'''
from sh import mount
mount("/dev/", "/mnt/test", "-t ext4")

#https://stackoverflow.com/questions/1667257/how-do-i-mount-a-filesystem-using-python
#As others have pointed out, there is no built-in mount function.
#However, it is easy to create one using ctypes, and this is a bit
#lighter weight and more reliable than using a shell command.
#Here's an example:

import ctypes
import ctypes.util
import os

libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
libc.mount.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong, ctypes.c_char_p)

def mount(source, target, fs, options=''):
  ret = libc.mount(source.encode(), target.encode(), fs.encode(), 0, options.encode())
  if ret < 0:
    errno = ctypes.get_errno()
    raise OSError(errno, f"Error mounting {source} ({fs}) on {target} with options '{options}': {os.strerror(errno)}")

mount('/dev/sdb1', '/mnt', 'ext4', 'rw')

'''
