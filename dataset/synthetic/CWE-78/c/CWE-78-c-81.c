#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static int read_token(char *out, size_t cap) {
    if (!fgets(out, cap, stdin)) return 0;
    size_t n = strlen(out);
    while (n && (out[n-1] == '\n' || out[n-1] == '\r')) out[--n] = '\0';
    return n > 0;
}

static int run_exec(const char *tool, char *const argv[]) {
    pid_t pid = fork();
    if (pid < 0) return 1;
    if (pid == 0) {
        execvp(tool, argv);
        _exit(127);
    }
    int st = 0;
    if (waitpid(pid, &st, 0) < 0) return 1;
    return (WIFEXITED(st) && WEXITSTATUS(st) == 0) ? 0 : 1;
}

int main(void) {
    char cmd[64];
    if (!read_token(cmd, sizeof(cmd))) return 1;

    if (strcmp(cmd, "net") == 0) {
        char *a[] = { "uname", "-n", NULL };
        return run_exec("uname", a);
    }
    if (strcmp(cmd, "kern") == 0) {
        char *a[] = { "uname", "-r", NULL };
        return run_exec("uname", a);
    }

    char *a[] = { "id", NULL };
    return run_exec("id", a);
}