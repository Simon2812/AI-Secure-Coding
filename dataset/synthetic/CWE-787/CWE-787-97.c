#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int bucket[16];
} collection;

static int read_count(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void gather(collection *c, int count)
{
    int temp[6];
    int i;
    int written = 0;

    for (i = 0; i < 6; i++)
    {
        temp[i] = i * 8;
    }

    if (count < 0)
    {
        return;
    }

    while (written < count && written < (int)(sizeof(c->bucket) / sizeof(c->bucket[0])))
    {
        int idx = written % 6;
        c->bucket[written] = temp[idx];
        written++;
    }
}

static void show_collection(const collection *c)
{
    int i;

    for (i = 0; i < 16; i++)
    {
        printf("%d\n", c->bucket[i]);
    }
}

int main(void)
{
    collection c;
    int count;

    memset(&c, 0, sizeof(c));

    printf("count:\n");
    count = read_count();

    gather(&c, count);
    show_collection(&c);

    return 0;
}