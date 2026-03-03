#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static int valid(const char *s)
{
    for (const unsigned char *p = (const unsigned char *)s; *p; ++p) {
        if (!(isalnum(*p) || *p == '.' || *p == '_' || *p == '-'))
            return 0;
    }
    return 1;
}

int main(int argc, char **argv)
{
    const char *f = (argc >= 2) ? argv[1] : "file.txt";
    if (!valid(f)) return 1;

    char cmd[256];
    snprintf(cmd, sizeof(cmd), "cat -- %s", f);

    return system(cmd) == 0 ? 0 : 1;
}