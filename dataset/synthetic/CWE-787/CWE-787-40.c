#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int read_index(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void record_event(int *logbuf, int index)
{
    int *cursor = logbuf + index;
    *cursor = 77;
}

static void dump_log(const int *logbuf, int size)
{
    int i;

    for (i = 0; i < size; i++)
    {
        printf("%d\n", logbuf[i]);
    }
}

int main(void)
{
    int logbuf[6] = {0};
    int index;

    printf("index:\n");
    index = read_index();

    record_event(logbuf, index);
    dump_log(logbuf, 6);

    return 0;
}