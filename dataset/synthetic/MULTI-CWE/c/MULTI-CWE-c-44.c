#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char path[128] = ".";
    char label[64] = "entry";
    int limit = 5;
    int i;

    if (argc > 1)
    {
        snprintf(path, sizeof(path), "%s", argv[1]);
    }

    if (argc > 2)
    {
        int v = atoi(argv[2]);
        if (v > 0 && v < 100)
        {
            limit = v;
        }
    }

    for (i = 0; i < limit; i++)
    {
        char line[128];
        snprintf(line, sizeof(line), "%s-%d", label, i);
        printf("%s\n", line);
    }

    if (limit > 0 && limit < 200)
    {
        int *buf = (int *)malloc((size_t)limit * sizeof(int));
        if (buf != NULL)
        {
            for (i = 0; i < limit; i++)
            {
                buf[i] = i + 1;
            }

            printf("last=%d\n", buf[limit - 1]);

            free(buf);
        }
    }

    if (strcmp(path, ".") == 0)
    {
        execl("/bin/ls", "ls", "-1", path, (char *)NULL);
    }

    return 0;
}