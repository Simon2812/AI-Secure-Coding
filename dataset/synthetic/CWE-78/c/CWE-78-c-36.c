#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <path>\n", argv[0]);
        return 1;
    }

    const char *path = argv[1];
    if (path[0] == '\0') {
        fprintf(stderr, "Empty path\n");
        return 1;
    }

    char cmd[256];
    snprintf(cmd, sizeof(cmd), "ls -l %s", path);

    int rc = system(cmd);
    if (rc != 0) {
        fprintf(stderr, "Command failed\n");
        return 1;
    }

    return 0;
}