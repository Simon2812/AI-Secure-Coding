#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int values[20];
} table;

static int read_start(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static void slide_window(table *t, int start)
{
    int window[6];
    int i;

    for (i = 0; i < 6; i++)
    {
        window[i] = i * 4;
    }

    for (i = 0; i < 6; i++)
    {
        t->values[start + i] = window[i];
    }
}

static void print_table(const table *t)
{
    int i;

    for (i = 0; i < 20; i++)
    {
        printf("%d\n", t->values[i]);
    }
}

int main(void)
{
    table t;
    int start;

    memset(&t, 0, sizeof(t));

    printf("start position:\n");

    start = read_start();

    slide_window(&t, start);

    print_table(&t);

    return 0;
}