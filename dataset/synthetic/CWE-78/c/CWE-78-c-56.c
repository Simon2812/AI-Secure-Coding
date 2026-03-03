#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static int launch_bg(const char *target)
{
    char *cmd = NULL;
    if (asprintf(&cmd, "touch %s", target) < 0)
        return 1;

    pid_t pid = vfork();
    if (pid < 0) {
        free(cmd);
        return 1;
    }

    if (pid == 0) {
        execl("/bin/sh", "sh", "-c", cmd, (char *)NULL);
        _exit(127);
    }

    free(cmd);
    return 0;
}

int main(int argc, char **argv)
{
    if (argc != 2)
        return 1;

    return launch_bg(argv[1]);
}