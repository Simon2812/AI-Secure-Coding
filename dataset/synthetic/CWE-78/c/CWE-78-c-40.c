#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *build_command(const char *user) {
    char *cmd = NULL;
    size_t len = strlen(user) + 32;

    cmd = malloc(len);
    if (!cmd) {
        return NULL;
    }

    strcpy(cmd, "id ");
    strcat(cmd, user);

    return cmd;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <username>\n", argv[0]);
        return 1;
    }

    char *command = build_command(argv[1]);
    if (!command) {
        fprintf(stderr, "Memory error\n");
        return 1;
    }

    int rc = system(command);
    free(command);

    if (rc != 0) {
        fprintf(stderr, "Lookup failed\n");
        return 1;
    }

    return 0;
}