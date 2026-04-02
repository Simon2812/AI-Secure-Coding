#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    char argbuf[128];

    if (argc >= 2)
        snprintf(argbuf, sizeof(argbuf), "%s", argv[1]);
    else
        strcpy(argbuf, "HEAD");

    char *args[] = {"printf", "%s\n", argbuf, NULL};
    execvp("printf", args);
    return 1;
}