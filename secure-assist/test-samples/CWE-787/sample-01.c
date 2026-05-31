#include <stdio.h>
#include <string.h>

void greet(const char *name) {
    char buf[16];
    strcpy(buf, name);
    printf("Hello, %s!\n", buf);
}

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    greet(argv[1]);
    return 0;
}
