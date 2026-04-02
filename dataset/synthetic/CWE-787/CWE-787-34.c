#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int id;
    char label[16];
} entry;

static void import_items(const char *name)
{
    FILE *source = fopen(name, "r");
    char buffer[128];
    entry records[4];
    int amount = 0;
    int i;

    if (source == NULL)
    {
        return;
    }

    memset(records, 0, sizeof(records));

    if (fgets(buffer, sizeof(buffer), source) != NULL)
    {
        amount = atoi(buffer);
    }

    for (i = 0; i < amount; i++)
    {
        if (fgets(buffer, sizeof(buffer), source) == NULL)
        {
            break;
        }

        sscanf(buffer, "%d %15s", &records[i].id, records[i].label);
    }

    for (i = 0; i < 4; i++)
    {
        printf("%d %s\n", records[i].id, records[i].label);
    }

    fclose(source);
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        return 1;
    }

    import_items(argv[1]);
    return 0;
}