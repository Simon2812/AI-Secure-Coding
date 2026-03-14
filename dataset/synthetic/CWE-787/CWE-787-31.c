#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void load_metrics(const char *file_name)
{
    FILE *stream = fopen(file_name, "r");
    char row[256];
    int slots[8];
    int expected = 0;
    int pos = 0;

    if (stream == NULL)
    {
        return;
    }

    memset(slots, 0, sizeof(slots));

    if (fgets(row, sizeof(row), stream) != NULL)
    {
        expected = atoi(row);
    }

    if (fgets(row, sizeof(row), stream) != NULL)
    {
        char *piece = strtok(row, ",");

        while (piece != NULL && pos < expected)
        {
            slots[pos] = atoi(piece);
            pos++;
            piece = strtok(NULL, ",");
        }
    }

    for (pos = 0; pos < 8; pos++)
    {
        printf("%d\n", slots[pos]);
    }

    fclose(stream);
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }

    load_metrics(argv[1]);
    return 0;
}