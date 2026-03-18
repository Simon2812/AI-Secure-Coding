#include <stdio.h>
#include <limits.h>

static int should_trigger(int current, int baseline, int threshold)
{
    if (current - baseline > threshold)
        return 1;

    return 0;
}

int main(void)
{
    int current = -2000000000;
    int baseline = 1500000000;
    int threshold = 100;

    if (should_trigger(current, baseline, threshold))
        puts("alert");
    else
        puts("normal");

    return 0;
}