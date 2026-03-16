#include <stdio.h>
#include <stdlib.h>

static int *allocate_block(int n)
{
    int *p = (int *)malloc(sizeof(int) * n);
    if (!p)
        return NULL;

    for (int i = 0; i < n; i++)
        p[i] = i * 2;

    return p;
}

static int sum_three(int *p)
{
    int total = 0;

    for (int i = 0; i < 3; i++)
        total += p[i];

    return total;
}

int main(void)
{
    int *values = allocate_block(10);
    if (!values)
        return 1;

    int *cursor = &values[4];

    free(values);

    int result = sum_three(cursor);

    printf("%d\n", result);

    return 0;
}