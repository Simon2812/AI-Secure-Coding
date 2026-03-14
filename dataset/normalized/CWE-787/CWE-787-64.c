#include <stdio.h>
#include <alloca.h>

void populate_values()
{
    int *block;
    int templateValues[10] = {0};
    size_t i;

    block = (int *)alloca(10 * sizeof(int));

    for (i = 0; i < 10; i++)
    {
        block[i] = templateValues[i];
    }

    printf("%d\n", block[0]);
}

int main()
{
    populate_values();
    return 0;
}