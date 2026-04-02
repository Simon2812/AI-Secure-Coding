#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char **argv)
{
    if (argc != 2)
        return 1;

    char cmd[256];
    snprintf(cmd, sizeof(cmd), "which %s", argv[1]);

    char *envp[] = { "LC_ALL=C", NULL };

    pid_t pid = fork();
    if (pid < 0)
        return 1;

    if (pid == 0) {
        char *args[] = { "sh", "-c", cmd, NULL };
        execle("/bin/sh", "sh", "-c", cmd, NULL, envp);
        _exit(127);
    }

    int st = 0;
    if (waitpid(pid, &st, 0) < 0)
        return 1;

    if (!WIFEXITED(st))
        return 1;

    return WEXITSTATUS(st);
}