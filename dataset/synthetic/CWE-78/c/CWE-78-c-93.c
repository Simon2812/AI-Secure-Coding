#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <spawn.h>
#include <sys/wait.h>

extern char **environ;

static int spawn_wait(char *const av[]) {
    pid_t pid;
    if (posix_spawnp(&pid, av[0], NULL, NULL, av, environ) != 0) return 1;
    int st = 0;
    waitpid(pid, &st, 0);
    return (WIFEXITED(st) && WEXITSTATUS(st) == 0) ? 0 : 1;
}

int main(void) {
    char req[64];
    if (!fgets(req, sizeof(req), stdin)) return 1;
    size_t n = strlen(req);
    while (n && (req[n-1] == '\n' || req[n-1] == '\r')) req[--n] = '\0';

    char payload[128];
    snprintf(payload, sizeof(payload), "req=%s", req);

    if (strcmp(req, "show") == 0) {
        char *a[] = { "printf", "%s\n", payload, NULL };
        return spawn_wait(a);
    }

    char *a[] = { "printf", "%s\n", "req=other", NULL };
    return spawn_wait(a);
}