#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <alloca.h>

void copy_values()
{
    int *dest = NULL;

    dest = (int *)alloca(7);

    int source[7] = {0};

    memcpy(dest, source, 7*sizeof(int));

    printf("%d\n", dest[0]);
}

int main()
{
    copy_values();
    return 0;
}