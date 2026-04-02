#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    if (argc != 2)
        return 1;

    char envbuf[256];
    snprintf(envbuf, sizeof(envbuf), "TARGET=%s", argv[1]);
    putenv(envbuf);

    char cmd[512];
    snprintf(cmd, sizeof(cmd), "echo $TARGET | tr a-z A-Z");

    int rc = system(cmd);
    return (rc == 0) ? 0 : 1;
}