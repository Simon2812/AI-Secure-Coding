#include <stdio.h>
#include <string.h>
#include <alloca.h>

void copy_values()
{
    int *buffer;
    int source[44] = {0};

    buffer = (int *)alloca(44 * sizeof(int));

    memcpy(buffer, source, 44 * sizeof(int));

    printf("%d\n", buffer[0]);
}

int main()
{
    copy_values();
    return 0;
}