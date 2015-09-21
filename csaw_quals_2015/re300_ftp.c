/* ftp.c */

#define SIGALARM 0xe

void sigalarm_handler(int sig) {
    exit(1);
}

int main(int argc, char** argv) {
    socklen_t acptaddr_len; // -0x48(rbp)
    int listener; // -0x44(rbp)
    int sock; // -0x40(rbp)
    int pid; // -0x3c(rbp)
    char* errmsg; // -0x38(rbp)
    struct sockaddr bindaddr; // 0x30(rbp)
    struct sockaddr acptaddr; // 0x20(rbp)
    signal(SIGALARM, &sigalarm_handler);
    puts("[+] Creating Socket");
    listener = socket(2, 1, 0);
    if(!listener) {
        error("socket error");
    }
    puts("[+] Binding");
    bzero(bindaddr, 0x10);
    ((short*)&bindaddr)[0] = 2;
    ((short*)&bindaddr)[1] = htons(0x2eec); // 12012, port to listen on
    ((int*)&bindaddr)[1] = htons(0);
    if(!bind(listener, &bindaddr, 0x10)) {
        error("bind error");
    }
    puts("[+] Listening");
    if(!listen(listener, 5)) {
        error("listen error");
    }
    do {
        puts("[+] accept loop");
        acceptaddr_len = 0x10;
        if(!(sock = accept(listener, &acptaddr, &acptaddr_len))) {
            errmsg = malloc(0x1e);
            sprintf(errmsg, "accept errror %d", __errno_location());
            error(errmsg);
        }
        printf("[+] socket fd: %d.\n", sock);
        pid = fork();
        if(pid) {
            close(listener);
            do_stuff(sock);
            close(sock);
            exit(0);
        }
        close(sock);
    } while(1);
}

void send_(int sock, char* msg) {
    if(!send(sock, msg, strlen(msg))) {
        error("send error");
    }
}

char* recv_(int sock) {
    char* buf = malloc(0x201);
    if(!buf) {
        error("malloc error");
    }
    memset(buf, 0, 0x201);
    if(!recv(sock, buf, 0x200, 0)) {
        error("receive error");
    }
    return buf;
}

void do_stuff(int arg_sock) {
    // rsp -- 0x990 bytes for locals -- rbp
    int sock = arg_sock; // -0x984(rbp)
    int i; // -0x978(rbp)
    int len; // -0x974(rbp)
    char* p1, p2 // -0x970(rbp), -0x968(rbp)
    // -0x960(rbp), 1224 bytes total
    struct {
        int sock; // -0x960(rbp)
        char* something1; // -0x950(rbp)
        char* something2; // -0x948(rbp)
        char* username; // offset 0x20, -0x940(rbp)
        char* password; // offset 0x28
        char dir[1024]; // offset 0xc0
    } state;
    int logged_in; // -0x4a0(rbp), overlap with dir?
    char buf[0x80]; // -0x490(rbp)
    char directory[1024]; // -0x410(rbp)
    alarm(65);
    srand(time(0));
    memset(state, 0, 1224);
    state->sock = sock;
    if(getcwd(directory, 0x400)) {
        strcpy(state->dir, directory);
    } else {
        error("CWD");
    }
    send_(sock, "Welcome to FTP server\n");
    for(;; free(p2)) {
        memset(buf, 0, 0x80);
        p1 = p2 = recv_(sock);
        len = strlen(p1);
        for(i=0; (*p1 != ' ') && (i < len-1); i++) {
            buf[i] = *p1++;
        }
        if(*p1 == ' ') { p1++; }
        p1[strlen(p1)-1] = 0;
        if(!strncasecmp("USER", buf, 4)) {
            if(logged_in) {
                send_(sock, "Cannot change user  ");
                send_(sock, state->username);
                send_(sock, "\n");
                continue;
            } else {
                state->username = p1;
                state->something2 = p1;
                do_login(state);
                continue;
            }
        }
        if(!strncasecmp("PASS", buf, 4)) {
            send_(sock, "send user first.\n");
            continue;
        }
        if(!strncasecmp("HELP", buf, 4)) {
            send_(sock, "USER PASS PASV PORT\nNOOP REIN LIST SYST SIZE\nRETR STOR PWD CWD\n");
            continue;
        }
        if(!logged_in) {
            send_(sock, "login with USER first.\n");
            continue;
        }
        if(!strncasecmp("REIN", buf, 4)) {
            logged_in = 0;
            continue;
        }
        if(!strncasecmp("PORT", buf, 4)) {
            do_port(...);
        }
        if(!strncasecmp("PASV", buf, 4)) {
            do_pasv(...);
        }
        if(!strncasecmp("STOR", buf, 4)) {
            do_stor(...);
        }
        if(!strncasecmp("RETR", buf, 4)) {
            do_retr(...);
        }
        if(!strncasecmp("QUIT", buf, 4)) {
            do_quit(...);
        }
        if(!strncasecmp("LIST", buf, 4)) {
            do_list(...);
        }
        if(!strncasecmp("SYST", buf, 4)) {
            do_syst(...);
        }
        if(!strncasecmp("NOOP", buf, 4)) {
            do_noop(...);
        }
        if(!strncasecmp("PWD", buf, 4)) {
            do_pwd(...);
        }
        if(!strncasecmp("CWD", buf, 4)) {
            do_cwd(...);
        }
        if(!strncasecmp("RDF", buf, 4)) {
            state->something1 = p1;
            state->something2 = buf;
            do_rdf(state);
        }
    }
}

// 0x0040159b
void do_login(struct state* arg_state) {
    // rsp -- 0xc0 bytes for locals -- rbp
    struct state* s = arg_state; // -0xb8(rsp)
    int len; // -0xa8(rsp)
    char* p1; // -0xa0(rsp)
    char* p2; // -0x98(rsp)
    char buf[0x80]; // -0x90(rsp)
    memset(buf, 0, 0x80);
    send_(s->sock, "Please send password for user ");
    send_(s->sock, s->username);
    send_(s->sock, "\n");
    p1 = p2 = recv_(s->sock);
    len = strlen(p1);
    for(i=0; (*p1 != ' ') && (i < len-1); i++) {
        buf[i] = *p1++;
    }
    if(*p1 == ' ') { p1++; }
    if(strncasecmp("PASS", buf, 4)) {
        send_(s->sock, "login with USER PASS.\n");
        return;
    }
    s->password = p1;
    hash_password(s->password);
    if(!strncmp(s->username, "blankwall", 9) && hash_password(s->password) == 0xd386d209) {
        send_(s->sock, "logged in.\n");
        return;
        // 0x00401780: movl $0x66, 0x202c7e(%rip) // this pokes a global, but I don't know which/where it's used
    } else {
        send_(s->sock, "Invalid login credentials.\n");
    }
}

// 0x00401540
int hash_password(char* s) {
    int hash = 0x1505; // -0x4(rbp)
    int i; // -0x8(rbp)
    for(i=0; s[i] != 0; i++) {
/*
|      |   0x00401558    8b45fc         movl -4(%rbp), %eax
|      |   0x0040155b    c1e005         shll $5, %eax
|      |   0x0040155e    89c2           movl %eax, %edx
|      |   0x00401560    8b45fc         movl -4(%rbp), %eax
|      |   0x00401563    8d0c02         leal (%rdx, %rax), %ecx
|      |   0x00401566    8b45f8         movl -8(%rbp), %eax
|      |   0x00401569    4863d0         movslq %eax, %rdx
|      |   0x0040156c    488b45e8       movq -0x18(%rbp), %rax
|      |   0x00401570    4801d0         addq %rdx, %rax
|      |   0x00401573    0fb600         movzbl (%rax), %eax
|      |   0x00401576    0fbec0         movsbl %al, %eax
|      |   0x00401579    01c8           addl %ecx, %eax
|      |   0x0040157b    8945fc         movl %eax, -4(%rbp)
*/
/*
        eax = hash * 32;
        edx = eax;
        eax = hash;
        ecx = eax+edx;
        eax = i;
        ecx += s[i];
        hash = ecx;
*/
        hash = (hash*32 + hash) + s[i];
    }
    return hash;
}

/*
def check(s):
    h = 0x1505
    for c in s:
        h = (33*h + ord(c)) % (2**32)
    return h == 0xd386d209

'''
>>> [(chr(i), (h-i) / 33.0) for i in range(128) if (h-i) % 33 == 0]
[('\x12', 107540247.0), ('3', 107540246.0), ('T', 107540245.0), ('u', 107540244.0)]
'''

def generate():
    def aux(h, tail):
        if h <= 0x1505:
            return tail
        ret = []
        for (c, i) in [(chr(x), (h-x)/33) for x in range(255) if (h-x) % 33 == 0]:
            for s in tail:
                ret.extend(aux(i, [c + s]))
        return ret
    return aux(0xd386d209, [''])

def generate():
    import itertools
    chars = map(chr, range(0x20, 0x7f))
    any8 = itertools.imap(lambda cs: ''.join(cs), itertools.product(*[chars]*6))
    valid = itertools.ifilter(check, any8)
    return valid

y = generate()
list(itertools.islice(y, 0, 1))
*/

// 0x004025f8
void do_rdf(struct state* s) {
    char* buf = malloc(0x28); // -0x10(rbp)
    FILE* f; // -0x8(rbp)
    if(!(f = fopen("re_solution.txt", "r"))) {
        send_(s->sock, "Error reading RE flag please contact an organizer");
        return;
    }
    fread(buf, 0x28, f);
    send_(s->sock, buf);
}
