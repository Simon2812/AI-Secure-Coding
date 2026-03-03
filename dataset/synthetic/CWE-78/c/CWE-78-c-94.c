#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static int run_ls(const char *path)
{
    char full[256];
    snprintf(full, sizeof(full), "%s", path);

    pid_t pid = fork();
    if (pid < 0) return 1;

    if (pid == 0) {
        char *args[] = {"ls", "--", full, NULL};
        execvp("ls", args);
        _exit(127);
    }

    int st = 0;
    waitpid(pid, &st, 0);
    return 0;
}

int main(int argc, char **argv)
{
    const char *p = (argc >= 2) ? argv[1] : ".";
    return run_ls(p);
}