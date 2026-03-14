#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void process_records(const char *file)
{
    FILE *handle = fopen(file, "r");
    char line[128];
    int values[5];
    int total = 0;
    int i;

    if (handle == NULL)
    {
        return;
    }

    memset(values, 0, sizeof(values));

    if (fgets(line, sizeof(line), handle) != NULL)
    {
        total = atoi(line);
    }

    for (i = 0; i < total; i++)
    {
        if (fgets(line, sizeof(line), handle) == NULL)
        {
            break;
        }

        values[i] = atoi(line);
    }

    for (i = 0; i < 5; i++)
    {
        printf("%d\n", values[i]);
    }

    fclose(handle);
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }

    process_records(argv[1]);
    return 0;
}