#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static int execute_template(const char *template, const char *value) {
    char cmd[512];

    snprintf(cmd, sizeof(cmd), template, value);

    pid_t pid = fork();
    if (pid < 0) {
        return 1;
    }

    if (pid == 0) {
        char *args[] = {"sh", "-c", cmd, NULL};
        execv("/bin/sh", args);
        _exit(127);
    }

    int status = 0;
    waitpid(pid, &status, 0);

    if (!WIFEXITED(status)) {
        return 1;
    }

    return WEXITSTATUS(status);
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <file>\n", argv[0]);
        return 1;
    }

    const char *template = getenv("CHECK_TEMPLATE");
    if (!template) {
        template = "wc -l %s";
    }

    return execute_template(template, argv[1]);
}