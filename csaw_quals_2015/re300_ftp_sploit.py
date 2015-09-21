#!/usr/bin/env python
# nc 54.175.183.202 12012
from pwn import *
import IPython

host = 'localhost' if '--live' not in sys.argv else '54.175.183.202'

p1 = remote(host, 12012)

p1.sendline('USER blankwall')
print(p1.recvuntil(['Please send password for user blankwall']))
p1.sendline('PASS cookie')
print(p1.recvuntil(['logged in']))

'''
p1.sendline('PASV')
port_pattern = 'PASV succesful listening on port: ([0-9]+)\n'
has_port = p1.recvregex(port_pattern)
print(has_port)
port = int(re.findall(port_pattern, has_port)[0], 10)

#p1.sendline('LIST')
#p1.sendline('RETR')
#p1.sendline('flag.txt')
#p1.send('RETRflag.txt')
#p1.send('RETRre_solution.txt')

print('nc %s %d' % (host, port))
#p2 = remote(host, port)
'''
p1.sendline('RDF')
p1.interactive()

'''
avi@debian:~/Documents/csaw_quals_2015_09$ ./re300_ftp_exploit.py --live
[+] Opening connection to 54.175.183.202 on port 12012: Done
Welcome to FTP server
Please send password for user blankwall

logged in
[*] Switching to interactive mode

flag{n0_c0ok1e_ju$t_a_f1ag_f0r_you}
$
'''
