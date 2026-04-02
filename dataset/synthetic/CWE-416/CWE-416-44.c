#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *label;
    int weight;
} Record;

static Record *create_record(const char *text, int weight)
{
    Record *r = (Record *)malloc(sizeof(Record));
    if (!r)
        return NULL;

    r->label = (char *)malloc(strlen(text) + 1);
    if (!r->label)
    {
        free(r);
        return NULL;
    }

    strcpy(r->label, text);
    r->weight = weight;

    return r;
}

static int measure_record(const Record *r)
{
    int total = r->weight;

    for (size_t i = 0; r->label[i] != '\0'; i++)
        total += r->label[i];

    return total;
}

void process_record()
{
    Record *item = create_record("delta", 4);
    if (!item)
        return;

    int score = measure_record(item);

    printf("%d\n", score);

    int guard = score % 3;

    free(item->label);
    free(item);

    if (guard < 0)
        puts("skip");
}