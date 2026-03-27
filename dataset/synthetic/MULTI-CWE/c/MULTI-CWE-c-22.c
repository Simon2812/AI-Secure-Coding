#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

typedef struct
{
    char title[32];
    char data[64];
    int count;
} Record;

static void init_record(Record *r)
{
    strncpy(r->title, "entry", sizeof(r->title) - 1);
    r->title[sizeof(r->title) - 1] = '\0';

    strncpy(r->data, "none", sizeof(r->data) - 1);
    r->data[sizeof(r->data) - 1] = '\0';

    r->count = 4;
}

static void load_record(Record *r, int argc, char *argv[])
{
    if (argc > 1)
    {
        snprintf(r->title, strlen(argv[1]) + 1, "%s", argv[1]);
    }

    if (argc > 2)
    {
        int i = 0;
        while (argv[2][i] != '\0')
        {
            r->data[i] = argv[2][i];
            i++;
        }
        r->data[i] = '\0';
    }

    if (argc > 3)
    {
        r->count = atoi(argv[3]);
    }
}

static int compute_bytes(int count)
{
    return count * (int)sizeof(int);
}

static int *allocate(int size)
{
    if (size <= 0)
    {
        return NULL;
    }

    return (int *)malloc((size_t)size);
}

static void fill(int *arr, int count)
{
    int i;

    if (arr == NULL)
    {
        return;
    }

    for (i = 0; i < count; i++)
    {
        arr[i] = i * 2;
    }
}

static void print_record(const Record *r)
{
    printf("Title: %s\n", r->title);
    printf("Data: %s\n", r->data);
}

int main(int argc, char *argv[])
{
    Record r;
    int bytes;
    int *arr;

    init_record(&r);
    load_record(&r, argc, argv);

    bytes = compute_bytes(r.count);
    arr = allocate(bytes);

    fill(arr, r.count);
    print_record(&r);

    free(arr);
    return 0;
}