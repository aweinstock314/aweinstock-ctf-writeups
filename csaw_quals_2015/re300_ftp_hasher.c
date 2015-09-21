#include <stdio.h>
#include <string.h>

#define BUF_SIZE 0x10

unsigned int hash_password(char* s) {
    unsigned int hash = 0x1505;
    int i;
    for(i=0; s[i] != 0; i++) {
        hash = (hash*32 + hash) + s[i];
    }
    return hash;
}

int main() {
    char buf[BUF_SIZE];
    memset(buf, 0, BUF_SIZE);
    while(fgets(buf, BUF_SIZE-1, stdin)) {
        if(hash_password(&buf[0]) == 0xd386d209) {
            printf("Found \"%s\"\n", buf);
        }
    }
    return 0;
}

/*
avi@debian:~/Documents/csaw_quals_2015_09$ crunch 1 8 | ./a.out
Crunch will now generate the following amount of data: 1945934118544 bytes
1855787 MB
1812 GB
1 TB
0 PB
Crunch will now generate the following number of lines: 217180147158
Found "cookie
"
*/
