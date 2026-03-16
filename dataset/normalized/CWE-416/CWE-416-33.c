#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int first;
    int second;
} Pair;

static void report_pair(const Pair *p)
{
    printf("%d,%d\n", p->first, p->second);
}

static void dispatch_frame()
{
    Pair *entries = NULL;

    entries = (Pair *)malloc(64 * sizeof(Pair));
    if (!entries)
    {
        exit(EXIT_FAILURE);
    }

    for (size_t idx = 0; idx < 64; ++idx)
    {
        entries[idx].first = 1;
        entries[idx].second = 2;
    }

    int flag = 1;

    if (flag)
    {
        report_pair(&entries[0]);
    }

    free(entries);
}

int main()
{
    dispatch_frame();
    return 0;
}