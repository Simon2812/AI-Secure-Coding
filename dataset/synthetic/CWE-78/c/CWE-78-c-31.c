#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void print_help(const char *name) {
    printf("Usage: %s <directory>\n", name);
    printf("Creates a compressed archive of the given directory.\n");
}

static int create_archive(const char *directory) {
    char command[512];

    /* Build tar command */
    snprintf(command, sizeof(command), "tar -czf backup.tgz %s", directory);

    /* Execute system command */
    int result = system(command);

    if (result != 0) {
        fprintf(stderr, "Archive creation failed\n");
        return -1;
    }

    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        print_help(argv[0]);
        return 1;
    }

    const char *dir = argv[1];

    if (strlen(dir) == 0) {
        fprintf(stderr, "Empty directory name\n");
        return 1;
    }

    return create_archive(dir);
}