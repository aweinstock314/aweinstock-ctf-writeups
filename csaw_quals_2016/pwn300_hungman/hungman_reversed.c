// 0x602100
char global_highscores[0x200];
// 0x602300
int global_score;
// 0x6020e0
struct user_t *global_user;

// sizeof(struct user_t) == 0x80 (known from malloc in initialize)
struct user_t {
    int32_t score;      // offset 0x00
    int32_t size;       // offset 0x04
    char* name;         // offset 0x08
    char has_tried[26]; // offset 0x10
};

// 0x00400f2d
struct user_t* initialize() {
    char name[0xf8];  // rbp-0x110
    struct user_t *q; // rbp-0x118
    char *p;          // rbp-0x120
    size_t size;      // rbp-0x124
    write(1, "What's your name?", 0x12);
    memset(name, 0, 0xf8);
    size = read(0, name, 0xf7);
    if((p = strchr(name, '\n')) != 0) {
        *p = 0;
    }
    p = malloc(size);
    q = malloc(0x80);
    memset(q, 0, 0x80);
    q->name = p;
    q->size = size;
    memcpy(p, name, size);
    return q;
}

// 0x00400b3a
void play_game(struct user_t *user, int fd) {
    char* tmp;       // rbp-0x08
    char* newname;   // rbp-0x10
    char *p;         // rbp-0x18
    int m;           // rbp-0x20
    int j;           // rbp-0x28
    int i;           // rbp-0x30
    int readsize;    // rbp-0x34
    int k;           // rbp-0x38
    size_t size;     // rbp-0x3c
    int num_correct; // rbp-0x40
    char tries;      // rbp-0x44
    char updatename; // rbp-0x45
    char c;          // rbp-0x46
    // user spilled to  rbp-0x58
    // fd spilled to    rbp-0x5c

    size = user->size;
    if((p = malloc(size)) == 0) {
        return;
    }
    read(fd, p, size);
    for(i=0; size-1 > i; i++) {
        p[i] ^= user->name[i]; // 0x00400b90 -> 0x00400bbd
        /*rsi = &p[i]
        rdx = rax = p[i]
        rax <<= 2;
        rax += rdx;
        rax <<= 4; */
        // Ignore the details of how username gets shuffled into randomness for now
        // it looks like a 0x61=='a' and 0x1a==26 involved, maybe clamp to lowercase?
    }
    tries = 3;
    num_correct = 0;
    c = '_';
    // this loop body spans from 0x00400c2b to 0x00400dc5
    while(tries > 0) {
        for(j=0; size-1 > j; j++) {
            if(user->has_tried[p[j] - 'a']) {
                write(1, p[j], 1);
            } else {
                write(1, "_", 1);
            }
        }
        write(1, "\n", 1)
        scanf(" %c", &c);
        if(c < 'a' || c > 'z') {
            puts("nope");
            tries--;
            continue;
        }
        if(user->has_tried[c - 'a']) {
            puts("nope");
            tries--;
            continue;
        }
        k = num_correct; // rbp-0x40
        m = 0; // rbp-0x20
        // loop from 0x00400d22 to 0x00400d6c
        for(; size-1 > m ; m++) {
            if(p[m] != c) {
                continue;
            }
            user->has_tried[c-'a'] = 1;
            num_correct++;
        }
        if(k == num_correct) {
            tries--;
        }
        if(size-1 > num_correct) {
            continue;
        }
        // this line involves xmm registers/float ops, I'm not sure it's correct
        user->score += (size-1)*0.25*32.0;
        goto skip_second_scoreupdate;
    }
    // it looks like this is the score for if you lose?
    user->score += 0.25*(size-1)*num_correct;
    skip_second_scoreupdate:
    if(user->score > global_score) {
        puts("High score! change name?");
        scanf(" %c", &updatename);
        if(updatename == 'y') {
            newname = malloc(0xf8);
            memset(newname, 0, 0xf8);
            readsize = read(0, newname, 0xf8);
            if((tmp = strchr(newname, '\n')) != 0) {
                tmp = 0;
            }
            memcpy(user->name, newname, readsize);
            free(newname);
        }
        snprintf(global_highscores, 0x200, "Highest player: %s", user->name);
        global_score = user->score;
    }
    memset(user->has_tried, 0, 26);
    free(p)
}

int main() {
    int fd;
    int choice;
    setvbuf(stdin, 0, 2, 0);
    memset(global_highscores, 0, 0x200);
    memcpy(global_highscores, "Default Highscore ", 0x14);
    global_score = 0x40;
    if((fd = open("/dev/urandom", 0)) == -1) {
        exit(1);
    }
    global_user = initialize();
    printf("Welcome, %s.\n", global_user->name);
    do {
        play_game(global_user, fd);
        printf("%s", global_highscores);
        printf("score: %d\n", global_score);
        printf("Continue? ");
        scanf(" %c", &choice);
    } while(choice != 'n');
    close(fd);
    return 0;
}
