#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int bucket[8];
} store;

static int read_count(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static void populate(store *s, int count)
{
    int i;

    for (i = 0; i < count; i++)
    {
        s->bucket[i] = i * 10;
    }
}

static void print_store(const store *s)
{
    int i;

    for (i = 0; i < 8; i++)
    {
        printf("%d\n", s->bucket[i]);
    }
}

int main(void)
{
    store s;
    int count;

    memset(&s, 0, sizeof(s));

    printf("count:\n");
    count = read_count();

    populate(&s, count);
    print_store(&s);

    return 0;
}