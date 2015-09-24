/* contacts.c */
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

struct node {
    //char data[0x50];
    char* desc; // offset 0x00
    char* phone; // offset 0x04
    char name[0x40]; // offset 0x08
    uint32_t desc_len; // offset 0x48
    uint32_t in_use; // offset 0x4c
};

uint32_t con_cnt = 0; // eip-relative in 64-bit, 0x0804b088 in 32-bit

struct node head[10]; // 0x6020c0 in 64-bit, 0x804b0a0 in 32-bit

const char* menu = "Menu:\n1)Create contact\n2)Remove contact\n3)Edit contact\n4)Display contacts\n5)Exit\n>>> ";

int main(int argc, char** argv) {
    setvbuf(stdin, 0, 2, 0);
    uint32_t i;
    uint32_t choice;
    for(i=0; i <= 9; i++) {
        //memset(NODE_HEAD+88*i, 0, 88); // 88 == 0x58
        memset(head[i], 0, sizeof(struct node));
    }
    printf("%s", menu);
    scanf("%u%*c", &choice);
    switch(choice) {
        case 1: createCon(head); break;
        case 2: removeCon(head); break;
        case 3: editCon(head); break;
        case 4: printCon(head); break;
        default: puts("Invalid option"); break;
    }
    puts("Thanks for trying out the demo, sadly your contacts are now erased");
    return 0;
}

int createCon(struct node* arg_head) {
    struct node* loc_head = arg_head; // -0x18(rbp)
    struct node* n = loc_head; // -0x08(rbp)
    int i = 0; // -0x0c(rbp)
    while(node->in_use && i <= 9) {
        node += sizeof(struct node);
        i++;
    }
    puts("Contact info: ");
    get_name(node);
    get_phone(node);
    get_desc(node);
    node->in_use = 1;
    con_cnt++;
    return con_cnt;
}

void get_name(struct node* n) {
    printf("\tName: ");
    fgets(n->name, 0x40, stdin);
    if(strchr(n->name, '\n') != 0) {
        *strchr(n->name, '\n') = 0;
    }
}

void get_phone(struct node* n) {
    printf("[DEBUG] Haven't written a parser for phone numbers; ");
    printf("You have 10 numbers");
    n->phone = malloc(11);
    if(n->phone == 0) {
        exit(1);
    }
    printf("\tEnter Phone No: ");
    fgets(n->phone, 11, stdin);
    if(strchr(n->phone, '\n') != 0) {
        *strchr(n->phone, '\n') = 0;
    }
}

void get_desc(struct node* n) {
    uint32_t desc_len; // -0x0c(ebp)
    printf("\tLength of description: ");
    scanf("%u%*c", &desc_len);
    n->desc_len = desc_len;
    malloc(desc_len+1);
    printf("\tEnter description:\n\t\t");
}

void removeCon(struct node* arg_head) {
    // esp -- 0x70 byte locals -- ebp
    struct node* loc_head = arg_head; // -0x68(rbp)
    size_t i; // -0x5c(rbp)
    struct node* n = loc_head; // -0x58(rbp)
    char buf[0x40]; // -0x50(rbp)
    printf("Name to remove? ");
    fgets(buf, 0x40, stdin);
    if(strchr(buf, '\n') != 0) {
        *strchr(buf, '\n') = 0;
    }
    for(i=0; i<9; i++, n += sizeof(struct node)) {
        if(!strcmp(n->name, buf)) {
            memset(n->name, 0, 0x40);
            free(n->desc);
            n->desc_len = 0;
            n->in_use = 0;
            con_cnt--;
            printf("Removed: %s..", buf);
        }
    }
    puts("Name not found dude");
}

void editCon(struct node* arg_head) {
    // esp -- 0x78 byte locals -- ebp
    struct node* loc_head = arg_head; // -0x6c(ebp)
    uint32_t desc_len; // -0x5c(ebp)
    uint32_t choice; // -0x58(ebp)
    struct node n = loc_head; // -0x54(ebp)
    size_t i; // -0x50(ebp)
    char buf[0x40]; // -0x4c(ebp)
    puts("Name to change? ");
    fgets(buf, 0x40, stdin);
    if(strchr(buf, '\n') != 0) {
        *strchr(buf, '\n') = 0;
    }
    for(i=0; i<9; i++, n += sizeof(struct node)) {
        if(!strcmp(buf, n->name)) {
            puts("1.Change name\n2.Change description\n>>> ");
            scanf("%u%*c", &choice);
            if(choice == 1) {
                printf("New name: ");
                fgets(buf->name, desc_len, stdin); // desc_len uninitialized on this path
                if(strchr(buf->name, '\n') != 0) {
                    *strchr(buf->name, '\n') = 0;
                }
                return;
            } else if(choice == 2) {
                free(buf->desc);
                printf("Length of description: ");
                scanf("%u%*c", &desc_len);
                printf("Description: ..");
                malloc(desc_len);
                fgets(buf->desc, desc_len, stdin);
                return;
            } else {
                puts("Bad option");
                return;
            }
        }
    }
    puts("Name not found");
}

void printCon(struct node* arg_head) {
    struct node* n = arg_head; // -0x10(ebp)
    uint32_t i = 0; // -0x0c(ebp)
    if(con_cnt == 0) {
        puts("Add contacts first");
        return;
    }
    puts("Contacts:");
    for(i=0; i<9; i++, n += sizeof(struct node)) {
        if(n->in_use) {
            printStuff(n->name, n->desc_len, n->phone, n->desc);
        }
    }
}

void printStuff(char* name, uint32_t desc_len, char* phone, char* desc) {
    printf("\tName: %s\n", name);
    printf("\tLength %u\n", desc_len);
    printf("\tPhone #: %s\n", phone);
    printf("\tDescription: ");
    printf(desc); // THIS IS PROBABLY THE VULN
}

