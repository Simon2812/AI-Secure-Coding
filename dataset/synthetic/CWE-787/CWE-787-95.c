#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    unsigned char shelf[22];
} container_space;

static int read_index(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static int normalize_index(int value)
{
    int idx;

    if (value < 0)
    {
        return -1;
    }

    idx = value;

    while (idx >= 22)
    {
        idx -= 22;
    }

    return idx;
}

static void commit_entry(container_space *space, int input)
{
    int slot = normalize_index(input);

    if (slot < 0)
    {
        return;
    }

    space->shelf[slot] = (unsigned char)(slot + 90);
}

static void display(const container_space *space)
{
    int i;

    for (i = 0; i < 22; i++)
    {
        printf("%u\n", space->shelf[i]);
    }
}

int main(void)
{
    container_space space;
    int index;

    memset(&space, 0, sizeof(space));

    printf("index:\n");
    index = read_index();

    commit_entry(&space, index);
    display(&space);

    return 0;
}