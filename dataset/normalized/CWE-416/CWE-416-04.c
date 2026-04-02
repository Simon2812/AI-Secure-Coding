#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int a;
    int b;
} Record;

static void display_record(const Record *r)
{
    printf("%d %d\n", r->a, r->b);
}

static void publish_record()
{
    Record *table = NULL;
    size_t idx;

    table = (Record *)malloc(80 * sizeof(Record));
    if (!table)
    {
        exit(EXIT_FAILURE);
    }

    for (idx = 0; idx < 80; idx++)
    {
        table[idx].a = 1;
        table[idx].b = 2;
    }

    free(table);

    display_record(&table[0]);
}

int main()
{
    publish_record();
    return 0;
}