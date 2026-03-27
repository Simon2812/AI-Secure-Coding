#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char path[128] = ".";
    char buf[64] = "log:";
    int i;

    if (argc > 1)
    {
        snprintf(path, sizeof(path), "%s", argv[1]);
    }

    if (argc > 2)
    {
        int n = atoi(argv[2]);
        if (n > 0 && n < 20)
        {
            for (i = 0; i < n; i++)
            {
                buf[strlen(buf)] = 'a' + (i % 26);
            }
            buf[strlen(buf)] = '\0';
        }
    }

    printf("%s\n", buf);

    if (strcmp(path, ".") != 0)
    {
        execl("/bin/ls", "ls", path, (char *)NULL);
    }

    return 0;
}