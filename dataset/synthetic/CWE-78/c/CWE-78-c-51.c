#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static int process_file(const char *path)
{
    FILE *f = fopen(path, "r");
    if (!f) {
        char cmd[256];
        snprintf(cmd, sizeof(cmd), "logger failed to open %s", path);
        return system(cmd);
    }

    char buf[128];
    while (fgets(buf, sizeof(buf), f)) {
        if (strstr(buf, "ERROR")) {
            printf("error line detected\n");
        }
    }

    fclose(f);
    return 0;
}

int main(int argc, char **argv)
{
    if (argc != 2)
        return 1;

    return process_file(argv[1]);
}