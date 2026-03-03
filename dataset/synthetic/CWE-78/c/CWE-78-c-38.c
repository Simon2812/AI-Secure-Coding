#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

typedef int (*runner_t)(const char *);

static int default_runner(const char *arg) {
    char buffer[256];
    snprintf(buffer, sizeof(buffer), "echo Processing %s", arg);

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        return 1;
    }

    if (pid == 0) {
        execl("/bin/sh", "sh", "-c", buffer, (char *)NULL);
        perror("execl");
        _exit(127);
    }

    int status = 0;
    if (waitpid(pid, &status, 0) < 0) {
        perror("waitpid");
        return 1;
    }

    return (WIFEXITED(status) && WEXITSTATUS(status) == 0) ? 0 : 1;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <value>\n", argv[0]);
        return 1;
    }

    runner_t run = default_runner;
    return run(argv[1]);
}