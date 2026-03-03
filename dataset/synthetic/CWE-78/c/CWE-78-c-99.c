#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int only_digits(const char *s)
{
    for (const unsigned char *p = (const unsigned char *)s; *p; ++p)
        if (*p < '0' || *p > '9')
            return 0;
    return 1;
}

int main(int argc, char **argv)
{
    const char *count = (argc >= 2) ? argv[1] : "3";
    if (!only_digits(count)) return 1;

    char cmd[128];
    snprintf(cmd, sizeof(cmd), "head -n %s /etc/passwd", count);

    return system(cmd) == 0 ? 0 : 1;
}
