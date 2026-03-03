#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static void append_arg(char *dst, size_t size, const char *arg) {
    strncat(dst, arg, size - strlen(dst) - 1);
}

static int execute_command(const char *cmd) {
    pid_t pid = fork();
    if (pid < 0) {
        return 1;
    }

    if (pid == 0) {
        execl("/bin/sh", "sh", "-c", cmd, (char *)NULL);
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
    char buffer[512] = "grep ";

    if (argc > 1) {
        append_arg(buffer, sizeof(buffer), argv[1]);
    } else {
        append_arg(buffer, sizeof(buffer), "root");
    }

    append_arg(buffer, sizeof(buffer), " /etc/passwd");

    return execute_command(buffer);
}