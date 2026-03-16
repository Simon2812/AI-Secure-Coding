#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *payload;
    int size;
} Item;

static void produce(Item *it)
{
    it->size = 6;
    it->payload = (char *)malloc(it->size + 1);
    if (!it->payload)
        exit(1);

    strcpy(it->payload, "HELLO");
}

static void stage_cleanup(Item *it)
{
    if (it->payload)
        free(it->payload);
}

static int checksum(Item *it)
{
    int s = 0;

    for (int i = 0; i < it->size; i++)
        s += it->payload[i];

    return s;
}

int main(void)
{
    Item obj;

    produce(&obj);

    char *alias = obj.payload;

    stage_cleanup(&obj);

    int res = 0;

    for (int i = 0; i < obj.size; i++)
        res += alias[i];

    return 0;
}