#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    unsigned char segments[48];
} region_store;

static int read_region(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void commit_region(region_store *store, int region)
{
    const int segment_size = 12;
    int start;
    int end;
    int i;

    if (region < 0)
    {
        return;
    }

    region = region % 4;

    start = region * segment_size;
    end = start + segment_size;

    for (i = start; i < end; i++)
    {
        store->segments[i] = (unsigned char)(i + 30);
    }
}

static void show_store(const region_store *store)
{
    int i;

    for (i = 0; i < 48; i++)
    {
        printf("%u\n", store->segments[i]);
    }
}

int main(void)
{
    region_store store;
    int region;

    memset(&store, 0, sizeof(store));

    printf("region:\n");
    region = read_region();

    commit_region(&store, region);
    show_store(&store);

    return 0;
}
