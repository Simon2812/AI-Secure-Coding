#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char area[26];
} storage_zone;

static int read_offset(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static int compute_slot(int value)
{
    int slot;

    if (value < 0)
    {
        return -1;
    }

    slot = value / 2;

    if (slot >= 26)
    {
        slot = slot % 26;
    }

    return slot;
}

static void write_symbol(storage_zone *zone, int input)
{
    int slot = compute_slot(input);

    if (slot < 0)
    {
        return;
    }

    zone->area[slot] = 'Z';
}

static void print_zone(const storage_zone *zone)
{
    int i;

    for (i = 0; i < 26; i++)
    {
        printf("%c\n", zone->area[i]);
    }
}

int main(void)
{
    storage_zone zone;
    int input;

    memset(&zone, 0, sizeof(zone));

    printf("value:\n");
    input = read_offset();

    write_symbol(&zone, input);
    print_zone(&zone);

    return 0;
}