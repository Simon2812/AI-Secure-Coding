#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    char command[256];

    sprintf(command, "cat %s", argv[1]);

    int ret = system(command);
    if (ret != 0) {
        printf("Command failed\n");
        return 1;
    }

    return 0;
}