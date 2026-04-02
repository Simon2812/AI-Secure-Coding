#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <spawn.h>
#include <sys/wait.h>

extern char **environ;

static int spawn_wait(char *const argv[]) {
    pid_t pid;
    if (posix_spawnp(&pid, argv[0], NULL, NULL, argv, environ) != 0) return 1;
    int st = 0;
    waitpid(pid, &st, 0);
    return (WIFEXITED(st) && WEXITSTATUS(st) == 0) ? 0 : 1;
}

int main(int argc, char **argv) {
    char tmpl[128] = "prefix-%s";
    const char *tag = (argc >= 2) ? argv[1] : getenv("TAG");
    if (!tag) tag = "none";

    char data[160];
    snprintf(data, sizeof(data), tmpl, tag);

    char *a[] = { "printf", "%s\n", data, NULL };
    return spawn_wait(a);
}