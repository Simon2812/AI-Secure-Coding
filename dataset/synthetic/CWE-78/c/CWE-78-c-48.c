#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

enum Action {
    ACT_NONE = 0,
    ACT_CLEAN = 1
};

static int read_line(char *buf, size_t cap)
{
    if (!fgets(buf, cap, stdin))
        return 0;
    size_t n = strlen(buf);
    while (n > 0 && (buf[n - 1] == '\n' || buf[n - 1] == '\r')) {
        buf[n - 1] = '\0';
        n--;
    }
    return 1;
}

static int do_clean(const char *path)
{
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "rm -f %s", path);

    pid_t pid = fork();
    if (pid < 0)
        return 1;

    if (pid == 0) {
        execlp("sh", "sh", "-c", cmd, (char *)NULL);
        _exit(127);
    }

    int st = 0;
    if (waitpid(pid, &st, 0) < 0)
        return 1;

    return (WIFEXITED(st) && WEXITSTATUS(st) == 0) ? 0 : 1;
}

int main(void)
{
    enum Action act = ACT_NONE;
    char input[256];

    printf("action (clean/quit): ");
    if (!read_line(input, sizeof(input)))
        return 1;

    if (strcmp(input, "quit") == 0)
        return 0;
    if (strcmp(input, "clean") == 0)
        act = ACT_CLEAN;

    if (act != ACT_CLEAN)
        return 1;

    printf("target: ");
    if (!read_line(input, sizeof(input)))
        return 1;

    if (input[0] == '\0') {
        fprintf(stderr, "empty target\n");
        return 1;
    }

    return do_clean(input);
}