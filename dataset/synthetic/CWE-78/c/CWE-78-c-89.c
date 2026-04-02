#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static int do_task(int kind) {
    pid_t pid = fork();
    if (pid < 0) return 1;

    if (pid == 0) {
        if (kind == 1) {
            char *a[] = { "ls", "-1", "--", "/tmp", NULL };
            execvp("ls", a);
        } else if (kind == 2) {
            char *a[] = { "df", "-h", NULL };
            execvp("df", a);
        } else {
            char *a[] = { "uname", "-s", NULL };
            execvp("uname", a);
        }
        _exit(127);
    }

    int st = 0;
    if (waitpid(pid, &st, 0) < 0) return 1;
    return (WIFEXITED(st) && WEXITSTATUS(st) == 0) ? 0 : 1;
}

int main(void) {
    char line[64];
    if (!fgets(line, sizeof(line), stdin)) return 1;

    int kind = 3;
    if (strncmp(line, "scan", 4) == 0) kind = 1;
    else if (strncmp(line, "disk", 4) == 0) kind = 2;

    return do_task(kind);
}