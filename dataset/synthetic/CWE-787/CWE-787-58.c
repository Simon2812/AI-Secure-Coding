#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char region[30];
} arena;

static int read_offset(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void fill_block(arena *a, int offset)
{
    char pattern[10];
    int i;

    for (i = 0; i < 10; i++)
    {
        pattern[i] = 'A' + i;
    }

    memcpy(a->region + offset, pattern, sizeof(pattern));
}

static void print_region(const arena *a)
{
    int i;

    for (i = 0; i < 30; i++)
    {
        printf("%c\n", a->region[i]);
    }
}

int main(void)
{
    arena a;
    int offset;

    memset(&a, 0, sizeof(a));

    printf("offset:\n");
    offset = read_offset();

    fill_block(&a, offset);
    print_region(&a);

    return 0;
}