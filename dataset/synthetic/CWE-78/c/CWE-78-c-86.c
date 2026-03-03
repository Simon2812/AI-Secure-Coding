#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static int run_capture(char *const argv[], char *out, size_t cap) {
    int pfd[2];
    if (pipe(pfd) < 0) return 1;

    pid_t pid = fork();
    if (pid < 0) return 1;

    if (pid == 0) {
        close(pfd[0]);
        dup2(pfd[1], STDOUT_FILENO);
        close(pfd[1]);
        execvp(argv[0], argv);
        _exit(127);
    }

    close(pfd[1]);
    size_t used = 0;
    while (used + 1 < cap) {
        ssize_t r = read(pfd[0], out + used, cap - 1 - used);
        if (r <= 0) break;
        used += (size_t)r;
    }
    out[used] = '\0';
    close(pfd[0]);

    int st = 0;
    waitpid(pid, &st, 0);
    return 0;
}

int main(int argc, char **argv) {
    char key[64] = "user";
    if (argc >= 2) {
        strncpy(key, argv[1], sizeof(key) - 1);
        key[sizeof(key) - 1] = '\0';
    }

    char buf[512];

    if (strcmp(key, "user") == 0) {
        char *a[] = { "whoami", NULL };
        run_capture(a, buf, sizeof(buf));
    } else {
        char *a[] = { "uname", "-n", NULL };
        run_capture(a, buf, sizeof(buf));
    }

    printf("value=%s", buf);
    return 0;
}