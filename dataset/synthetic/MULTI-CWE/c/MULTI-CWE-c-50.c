#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char path[128] = "input.log";
    int window = 5;
    int i;

    if (argc > 1)
    {
        snprintf(path, sizeof(path), "%s", argv[1]);
    }

    if (argc > 2)
    {
        int v = atoi(argv[2]);
        if (v > 0 && v < 50)
        {
            window = v;
        }
    }

    FILE *f = fopen(path, "r");
    if (f != NULL)
    {
        char line[256];
        int *last_values = (int *)malloc((size_t)window * sizeof(int));
        int idx = 0;
        int total = 0;

        if (last_values == NULL)
        {
            fclose(f);
            return 0;
        }

        while (fgets(line, sizeof(line), f) != NULL)
        {
            int val = (int)strtol(line, NULL, 10);

            last_values[idx % window] = val;
            idx++;

            if (idx >= window)
            {
                int j;
                total = 0;

                for (j = 0; j < window; j++)
                {
                    total += last_values[j];
                }

                printf("avg=%d\n", total / window);
            }
        }

        free(last_values);
        fclose(f);
    }

    if (strncmp(path, "input", 5) == 0)
    {
        execl("/usr/bin/tail", "tail", "-n", "3", path, (char *)NULL);
    }

    return 0;
}
