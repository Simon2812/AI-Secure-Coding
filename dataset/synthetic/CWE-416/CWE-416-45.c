#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int compute_sum(const int *arr, int n)
{
    int total = 0;

    for (int i = 0; i < n; i++)
        total += arr[i];

    return total;
}

int main(void)
{
    int count = 5;
    int *numbers = (int *)malloc(sizeof(int) * count);
    if (!numbers)
        return 1;

    for (int i = 0; i < count; i++)
        numbers[i] = i * 3;

    int snapshot[5];
    for (int i = 0; i < count; i++)
        snapshot[i] = numbers[i];

    free(numbers);

    int result = compute_sum(snapshot, count);

    printf("%d\n", result);

    if (result < 0)
        puts("skip");

    return 0;
}