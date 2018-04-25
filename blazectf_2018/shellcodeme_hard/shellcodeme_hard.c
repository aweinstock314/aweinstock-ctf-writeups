// gcc -Os shellcodeme_hard.c -o shellcodeme_hard
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <ucontext.h>
#include <unistd.h>

#define BUF_SIZE (0x4096 & ~(getpagesize()-1))

int main() {
    setbuf(stdout, NULL);
    unsigned char seen[257], *p, *buf, *stack;
    int random = open("/dev/urandom", O_RDONLY);
    memset(seen, 0, sizeof seen);
    buf = mmap(0, BUF_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    puts("Shellcode?");
    fgets(buf, BUF_SIZE, stdin);
    for(p=buf; *p != '\n'; p++) {
        seen[256] += !seen[*p];
        seen[*p] |= 1;
    }
    if(seen[256] > 7) {
        puts("Shellcode too diverse.");
        _exit(1);
    } else {
        mprotect(buf, BUF_SIZE, PROT_READ | PROT_EXEC);
        stack = mmap(0, BUF_SIZE, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        read(random, stack, BUF_SIZE-sizeof(ucontext_t));
        stack += BUF_SIZE;

        stack -= sizeof(ucontext_t);
        ucontext_t *c = (ucontext_t*)stack;
        getcontext(c);
        c->uc_stack.ss_sp = stack;
        c->uc_link = 0;
        makecontext(c, (void(*)(void))buf, 0);

        unsigned long *p, i=0;
        for(p = (unsigned long*)c->uc_mcontext.gregs; i < NGREG; i++) {
            if(i != 15 && i != 16) {
                read(random, &p[i], sizeof p[i]);
            }
            //printf("%d: 0x%016lx\n", i, p[i]);
        }
        close(random);
        setcontext((ucontext_t*)c);
        _exit(0);
    }
}
