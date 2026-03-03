#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <spawn.h>
#include <sys/wait.h>

extern char **environ;

static int read_line(char *b, size_t n) {
    if (!fgets(b, n, stdin)) return 0;
    size_t k = strlen(b);
    while (k && (b[k-1] == '\n' || b[k-1] == '\r')) b[--k] = '\0';
    return 1;
}

static int spawnp_wait(const char *file, char *const argv[]) {
    pid_t pid;
    if (posix_spawnp(&pid, file, NULL, NULL, argv, environ) != 0) return 1;
    int st = 0;
    if (waitpid(pid, &st, 0) < 0) return 1;
    return (WIFEXITED(st) && WEXITSTATUS(st) == 0) ? 0 : 1;
}

int main(void) {
    char req[80];
    if (!read_line(req, sizeof(req))) return 1;

    if (strcmp(req, "short") == 0) {
        char *a[] = { "uptime", "-p", NULL };
        return spawnp_wait("uptime", a);
    }
    if (strcmp(req, "full") == 0) {
        char *a[] = { "uptime", NULL };
        return spawnp_wait("uptime", a);
    }

    char *a[] = { "date", "-u", NULL };
    return spawnp_wait("date", a);
}