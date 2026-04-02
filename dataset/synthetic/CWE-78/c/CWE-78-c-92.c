#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static int attempt_run(int k) {
    pid_t pid = fork();
    if (pid < 0) return 1;

    if (pid == 0) {
        if (k == 0) {
            char *a[] = { "uname", "-a", NULL };
            execvp("uname", a);
        } else {
            char *a[] = { "id", NULL };
            execvp("id", a);
        }
        _exit(127);
    }

    int st = 0;
    if (waitpid(pid, &st, 0) < 0) return 1;
    return (WIFEXITED(st) && WEXITSTATUS(st) == 0) ? 0 : 1;
}

int main(int argc, char **argv) {
    int k = (argc >= 2 && strcmp(argv[1], "id") == 0) ? 1 : 0;

    int tries = 0;
    while (tries < 2) {
        if (attempt_run(k) == 0) return 0;
        tries++;
    }
    return 1;
}