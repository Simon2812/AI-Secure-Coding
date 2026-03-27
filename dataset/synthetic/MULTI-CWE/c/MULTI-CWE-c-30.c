#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void append_digits(char *buf, int n)
{
    int i;

    for (i = 0; i < n; i++)
    {
        buf[strlen(buf)] = '0' + (i % 10);
    }

    buf[strlen(buf)] = '\0';
}

static void run_cat(const char *path)
{
    char cmd[256] = "cat ";
    strcat(cmd, path);
    system(cmd);
}

int main(int argc, char *argv[])
{
    char path[128] = "/tmp";
    char base[64] = "data:";
    char *ptr;
    char *alias;
    int n = 3;

    if (argc > 1)
    {
        snprintf(path, sizeof(path), "%s", argv[1]);
    }

    if (argc > 2)
    {
        n = atoi(argv[2]);
    }

    ptr = (char *)malloc(n * 16);
    alias = ptr;

    if (ptr != NULL)
    {
        strcpy(ptr, base);
        append_digits(ptr, n);
    }

    free(ptr);

    printf("%s\n", alias);

    if (n > 0)
    {
        run_cat(path);
    }

    return 0;
}