#include <stdio.h>
#include <limits.h>

static int compute_gap(int anchor, int reduction)
{
    if (anchor < INT_MIN + reduction)
        return anchor;

    return anchor - reduction;
}

int main(void)
{
    int anchor = -1800000000;
    int reduction = 100000000;

    int gap = compute_gap(anchor, reduction);
    printf("%d\n", gap);

    return 0;
}