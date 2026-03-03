#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char **argv)
{
    char cmd[256];

    if (argc >= 2)
        snprintf(cmd, sizeof(cmd), "%s", argv[1]);
    else
        strcpy(cmd, "status");

    pid_t pid = fork();
    if (pid < 0) return 1;

    if (pid == 0) {
        if (strcmp(cmd, "status") == 0) {
            char *a[] = {"systemctl", "status", "cron", NULL};
            execvp("systemctl", a);
        } else {
            char *a[] = {"systemctl", "is-active", "cron", NULL};
            execvp("systemctl", a);
        }
        _exit(127);
    }

    wait(NULL);
    return 0;
}