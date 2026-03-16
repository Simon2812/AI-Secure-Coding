#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int id;
    char *name;
} Record;

static Record *table[4];

static void register_record(int slot, Record *r)
{
    if (slot >= 0 && slot < 4)
        table[slot] = r;
}

static Record *lookup(int slot)
{
    if (slot < 0 || slot >= 4)
        return NULL;

    return table[slot];
}

static void destroy_record(Record *r)
{
    if (!r)
        return;

    if (r->name)
        free(r->name);

    free(r);
}

static int score_record(Record *r)
{
    int total = r->id;

    for (size_t i = 0; r->name[i] != '\0'; i++)
        total += r->name[i];

    return total;
}

int main(void)
{
    Record *rec = (Record *)malloc(sizeof(Record));
    if (!rec)
        return 1;

    rec->id = 5;

    rec->name = (char *)malloc(16);
    if (!rec->name)
    {
        free(rec);
        return 1;
    }

    strcpy(rec->name, "node");

    register_record(2, rec);

    destroy_record(rec);

    Record *ref = lookup(2);

    int result = score_record(ref);

    printf("%d\n", result);

    return 0;
}