#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    unsigned char buffer[30];
} decode_area;

static int read_blocks(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static void decode(decode_area *area, int blocks)
{
    unsigned char temp[5];
    int write_pos = 0;
    int i;
    int b;

    for (i = 0; i < 5; i++)
    {
        temp[i] = (unsigned char)(70 + i);
    }

    for (b = 0; b < blocks && write_pos < (int)sizeof(area->buffer); b++)
    {
        int remaining = sizeof(area->buffer) - write_pos;
        int limit = sizeof(temp);

        if (limit > remaining)
        {
            limit = remaining;
        }

        for (i = 0; i < limit; i++)
        {
            area->buffer[write_pos + i] = temp[i];
        }

        write_pos += limit;
    }
}

static void show(const decode_area *area)
{
    int i;

    for (i = 0; i < (int)sizeof(area->buffer); i++)
    {
        printf("%u\n", area->buffer[i]);
    }
}

int main(void)
{
    decode_area area;
    int blocks;

    memset(&area, 0, sizeof(area));

    printf("blocks:\n");
    blocks = read_blocks();

    decode(&area, blocks);
    show(&area);

    return 0;
}