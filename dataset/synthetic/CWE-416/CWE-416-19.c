#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *name;
    int id;
} Entry;

static void cleanup_name(Entry *e)
{
    if (e->name != NULL)
    {
        free(e->name);
    }
}

static int compare_entry(Entry *e)
{
    if (strcmp(e->name, "admin") == 0)
        return 1;
    return 0;
}

int main(void)
{
    Entry item;
    item.id = 7;

    item.name = (char *)malloc(16);
    if (item.name == NULL)
        return 1;

    strcpy(item.name, "admin");

    cleanup_name(&item);

    compare_entry(&item);

    return 0;
}