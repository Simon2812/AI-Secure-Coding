#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int capacity;
    int *data;
} heap_log;

static int read_count(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void allocate_log(heap_log *log)
{
    log->capacity = 8;
    log->data = (int *)malloc(log->capacity * sizeof(int));

    if (log->data != NULL)
    {
        memset(log->data, 0, log->capacity * sizeof(int));
    }
}

static void fill_entries(heap_log *log, int count)
{
    int *cursor = log->data;
    int i;

    for (i = 0; i < count; i++)
    {
        *cursor = i * 11;
        cursor++;
    }
}

static void print_log(const heap_log *log)
{
    int i;

    for (i = 0; i < log->capacity; i++)
    {
        printf("%d\n", log->data[i]);
    }
}

int main(void)
{
    heap_log log;
    int count;

    allocate_log(&log);

    if (log.data == NULL)
    {
        return 1;
    }

    printf("entry count:\n");
    count = read_count();

    fill_entries(&log, count);
    print_log(&log);

    free(log.data);

    return 0;
}