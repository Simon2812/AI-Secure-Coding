#include <stdio.h>
#include <stdlib.h>

static int *build_array(int n)
{
    int *arr = (int *)malloc(sizeof(int) * n);
    if (!arr)
        return NULL;

    for (int i = 0; i < n; i++)
        arr[i] = i + 2;

    return arr;
}

static void release_array(int *p)
{
    free(p);
}

static int multiply(const int *values, int n)
{
    int r = 1;

    for (int i = 0; i < n; i++)
        r *= (values[i] + 1);

    return r;
}

int main(void)
{
    int *values = build_array(4);
    if (!values)
        return 1;

    int backup[4];

    for (int i = 0; i < 4; i++)
        backup[i] = values[i];

    release_array(values);

    int result = multiply(backup, 4);

    return result % 5;
}
