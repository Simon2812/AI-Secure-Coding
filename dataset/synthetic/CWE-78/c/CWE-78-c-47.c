#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static int run_once(const char *arg)
{
    char buf[256];
    int attempt = 0;

retry:
    snprintf(buf, sizeof(buf), "whois %s", arg);

    pid_t pid = fork();
    if (pid < 0)
        return 1;

    if (pid == 0) {
        execlp("sh", "sh", "-c", buf, (char *)NULL);
        _exit(127);
    }

    int st = 0;
    if (waitpid(pid, &st, 0) < 0)
        return 1;

    if (!WIFEXITED(st) && attempt == 0) {
        attempt++;
        goto retry;
    }

    return (WIFEXITED(st) && WEXITSTATUS(st) == 0) ? 0 : 1;
}

int main(int c, char **v)
{
    if (c != 2)
        return 1;

    return run_once(v[1]);
}