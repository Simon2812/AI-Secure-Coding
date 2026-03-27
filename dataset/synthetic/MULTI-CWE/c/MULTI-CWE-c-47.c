#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char input[128];
    char prefix[32] = "item";
    int limit = 6;
    int i;

    input[0] = '\0';

    if (argc > 1)
    {
        snprintf(input, sizeof(input), "%s", argv[1]);
    }

    if (argc > 2)
    {
        int v = atoi(argv[2]);
        if (v > 0 && v < 40)
        {
            limit = v;
        }
    }

    {
        char *view = input;
        size_t len = strlen(view);

        if (len > 10)
        {
            view += (len - 10);
        }

        for (i = 0; i < limit; i++)
        {
            char line[64];
            snprintf(line, sizeof(line), "%s:%s:%d", prefix, view, i);
            printf("%s\n", line);
        }
    }

    if (limit > 0 && limit < 80)
    {
        int *data = (int *)malloc((size_t)limit * sizeof(int));
        if (data != NULL)
        {
            for (i = 0; i < limit; i++)
            {
                data[i] = (i + 1) * (i % 3 + 1);
            }

            if (limit > 2)
            {
                printf("sample=%d\n", data[2]);
            }

            free(data);
        }
    }

    if (prefix[0] == 'i')
    {
        execl("/bin/echo", "echo", "ok", (char *)NULL);
    }

    return 0;
}