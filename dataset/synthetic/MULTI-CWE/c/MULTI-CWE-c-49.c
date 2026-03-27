#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int is_valid_range(int n)
{
    return (n > 0 && n < 100);
}

int main(int argc, char *argv[])
{
    char name[64] = "default";
    int limit = 10;
    int i;

    if (argc > 1)
    {
        snprintf(name, sizeof(name), "%s", argv[1]);
    }

    if (argc > 2)
    {
        int parsed = atoi(argv[2]);
        if (is_valid_range(parsed))
        {
            limit = parsed;
        }
    }

    {
        char *cursor = name;
        size_t len = strlen(name);

        if (len > 5)
        {
            cursor += 2;
            len -= 2;
        }

        for (i = 0; i < limit; i++)
        {
            char out[96];
            snprintf(out, sizeof(out), "[%d] %.*s\n", i, (int)len, cursor);
            printf("%s", out);
        }
    }

    if (limit > 0 && limit < 120)
    {
        int *table = (int *)malloc((size_t)limit * sizeof(int));
        if (table != NULL)
        {
            for (i = 0; i < limit; i++)
            {
                table[i] = (i + 1) * (limit - i);
            }

            if (limit > 3)
            {
                printf("check=%d\n", table[3]);
            }

            free(table);
        }
    }

    if (name[0] != '\0')
    {
        execl("/bin/echo", "echo", name, (char *)NULL);
    }

    return 0;
}