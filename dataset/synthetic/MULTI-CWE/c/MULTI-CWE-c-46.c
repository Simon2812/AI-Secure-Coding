#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char base[64] = "val";
    char suffix[64];
    int repeat = 4;
    int i;

    if (argc > 1)
    {
        snprintf(suffix, sizeof(suffix), "%s", argv[1]);
    }
    else
    {
        suffix[0] = '\0';
    }

    if (argc > 2)
    {
        int t = atoi(argv[2]);
        if (t > 0 && t < 50)
        {
            repeat = t;
        }
    }

    for (i = 0; i < repeat; i++)
    {
        char out[128];
        snprintf(out, sizeof(out), "%s_%s_%d", base, suffix, i);
        printf("%s\n", out);
    }

    if (repeat > 0 && repeat < 100)
    {
        int *arr = (int *)malloc((size_t)repeat * sizeof(int));
        if (arr != NULL)
        {
            for (i = 0; i < repeat; i++)
            {
                arr[i] = i * 3;
            }

            printf("mid=%d\n", arr[repeat / 2]);

            free(arr);
            arr = NULL;
        }
    }

    if (strcmp(base, "val") == 0)
    {
        execl("/usr/bin/printf", "printf", "%s\n", "done", (char *)NULL);
    }

    return 0;
}