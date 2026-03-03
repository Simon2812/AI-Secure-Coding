#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <spawn.h>
#include <sys/wait.h>

extern char **environ;

static int run_cmd(const char *arg)
{
    char buf[256];
    snprintf(buf, sizeof(buf), "hostname %s", arg);

    char *argv[] = { "sh", "-c", buf, NULL };
    pid_t pid;
    if (posix_spawn(&pid, "/bin/sh", NULL, NULL, argv, environ) != 0)
        return 1;

    int st = 0;
    if (waitpid(pid, &st, 0) < 0)
        return 1;

    if (!WIFEXITED(st))
        return 1;

    return WEXITSTATUS(st);
}

int main(int argc, char **argv)
{
    if (argc != 2)
        return 1;

    return run_cmd(argv[1]);
}