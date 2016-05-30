/*
aaa
s main
afn sub.print_truck @ 0x00400783
afn sub.print_menu @ 0x00400793
afn sub.get_input @ 0x0040072d
afn sub.interpret_input @ 0x00400983
afn sub.view_order @ 0x004007a3
afn sub.create_order @ 0x00400821
afn sub.update_order @ 0x004008dc
*/

/*
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FORTIFY FORTIFIED FORTIFY-able  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No      0               4       delivery
*/
#include <stdio.h>
#include <stdint.h>
#include <string.h>

// order entries seem to be 2**10 = 1024 units long (shll $0xa, %eax is used to dereference stuff)
// 0x400 == 1024
char* global_buf; // 0x602080
int global_count = 0; // 0x60207c


void print_truck() {
    puts("--------------------------------------------------------------------\n"\
         "Bread Delivery As A Service\n"\
         "Shipping tracking interface\n"\
         "                   _________________________________________  \n"\
         "             _____|.-----..-----..-----..-----..----..-----.]\n"\
         "            /.--.|||;;;;;||;;;;;||;;;;;||;;;;;||;;;;||;;;;;||\n"\
         "           //   ||||;;;;;||;;;;;||;;;;;||;;;;;||;;;;||;;;;;||\n"\
         "  ___...--'|`---'|||BREAD||BREAD||BREAD||BREAD||;;;;||BREAD||\n"\
         " (=      | |   -'|||;;;;;||;;;;;||;;;;;||;;;;;||;;;;||;;;;;||\n"\
         " |  _..--' |____.'||;;;;;||;;;;;||;;;;;||;;;;;|'----'|;;;;;||\n"\
         " |-'.----.  _____ |'-----''-----''-----''-----'.----.'-----'|\n"\
         "|=./ .--. \\|=====||___________________________/ .--. \\______]\n"\
         "'=' :(--): `-----''--------------------------' :(--): `-----'\n"\
         "     `--'                                       `--'\n"\
         "");
}

void print_menu() {
    puts("\n-------------------------------------\n1: View order\n2: Add order\n3: Update order\n4: Exit\n-------------------------------------\n");
}

void get_input(char* buf, const char* prompt);
void view_order();
void create_order();
void update_order();
uint64_t interpret_input(char* input);

int main() {
    char buf[0x19000]; // rbp - 0x19010
    char input[0x400]; // rbp - 0x19410
    // 0x19000/1024 == 100
    uint32_t done = 0; // rbp - 4
    // if "done" is between buf and return address, can't leak libc (need to partial-overwrite low nibbles)
    // suggested rewrite to guarentee leak:
    /*
    struct {
        int done;
        char input[1024];
        char buf[1024*100];
    } locals;
    */
        

    memset(buf, 0, 0x19000);
    global_buf = &buf[0];

    print_truck();
    while(!done) {
        print_menu();
        get_input(input, "Your option");
        done = interpret_input(input);
    }
    return 0;
}

uint64_t interpret_input(char* input) {
    // looks like a switch compiled into an if-else chain
    switch(input[0]) {
        case '1':
            view_order();
            break;
        case '2':
            create_order();
            break;
        case '3':
            update_order();
            break;
        case '4':
            return 1;
        default:
            puts("\nInvalid option.\n");
            break;
    }
    return 0;
}

void view_order() {
    char* p = 0; // rbp - 0x8
    int i = 0; // rbp - 0xc
    p = &global_buf[i * 1024];
    while(*p) {
        printf("\nOrder no: %d\n-------------------------------------\n%s\n-------------------------------------\n\n", i+1, p);
        i++;
        p = &global_buf[i * 1024];
    }
    puts("End of order list.");
}

void update_order() {
    int i; // rbp - 0x4 (0x420 delivery2)
    uint32_t j; // rbp - 0x8 (0x41c delivery2)
    char* p; // rbp - 0x10 (0x418 delivery2)
    char buf[0x400]; // rbp - 0x410
    get_input(buf, "Order ID");
    i = atoi(buf)-1;
    get_input(buf, "Order information");
    j = strlen(buf);
    buf[j-1] = 0;
    p = &global_buf[i*1024];

    // This line is a bug that renders the challenge unsolvable.
    // to fix, replace with strncpy(p, buf, j);
    //strncpy(p, buf, 0x400);

    // updated(delivery2): 
    //strncpy(p, buf, j);
    // updated(delivery3)
    strncpy(p, buf, j-1);

    puts("\nOrder has been updated.");
}

// add_order in symboled version
void create_order() {
    uint32_t i; // rbp - 0x4 (0x41c delivery2)
    char* p; // rbp - 0x10 (0x418 delivery2)
    char buf[0x400]; // rbp - 0x410
    printf("Creating order no:%d\n", global_count+1);
    if(global_count <= 99) {
        get_input(buf, "Your order information");
        i = strlen(buf);
        buf[i-1] = 0;
        p = &global_buf[(global_count++)*1024];
        //strncpy(p, buf, 0x400);
        // updated(delivery2):
        strncpy(p, buf, i);
        puts("Order has been added.");
    } else {
        puts("Error: Order queue is full.");
        return;
    }
}

void get_input(char* buf, const char* prompt) {
    memset(buf, 0, 0x400);
    printf("%s: ", prompt);
    fgets(buf, 0x400, stdin);
}
