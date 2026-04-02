#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char zone[24];
} memory_area;

static int parse_offset(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static void place_marker(memory_area *area, int offset)
{
    char marker[6] = {'A','B','C','D','E','F'};
    int i;

    if (offset < 0)
    {
        return;
    }

    if (offset + sizeof(marker) > sizeof(area->zone))
    {
        return;
    }

    for (i = 0; i < (int)sizeof(marker); i++)
    {
        area->zone[offset + i] = marker[i];
    }
}

static void show_zone(const memory_area *area)
{
    int i;

    for (i = 0; i < (int)sizeof(area->zone); i++)
    {
        printf("%c\n", area->zone[i]);
    }
}

int main(void)
{
    memory_area area;
    int offset;

    memset(&area, 0, sizeof(area));

    printf("offset:\n");
    offset = parse_offset();

    place_marker(&area, offset);
    show_zone(&area);

    return 0;
}