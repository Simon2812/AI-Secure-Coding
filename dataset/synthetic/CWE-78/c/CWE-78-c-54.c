#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static int write_script(const char *arg)
{
    FILE *f = fopen("tmp.sh", "w");
    if (!f)
        return 1;

    fprintf(f, "#!/bin/sh\n");
    fprintf(f, "uptime %s\n", arg);
    fclose(f);

    return 0;
}

int main(int argc, char **argv)
{
    if (argc != 2)
        return 1;

    if (write_script(argv[1]) != 0)
        return 1;

    pid_t pid = fork();
    if (pid < 0)
        return 1;

    if (pid == 0) {
        execl("/bin/sh", "sh", "tmp.sh", (char *)NULL);
        _exit(127);
    }

    int st = 0;
    if (waitpid(pid, &st, 0) < 0)
        return 1;

    return (WIFEXITED(st) && WEXITSTATUS(st) == 0) ? 0 : 1;
}