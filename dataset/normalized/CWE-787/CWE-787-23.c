#include <stdio.h>
#include <string.h>

void copy_data()
{
    char *pointer;
    char buffer[100];

    memset(buffer, 'A', 99);
    buffer[99] = '\0';

    pointer = buffer - 8;

    char src[100];
    memset(src, 'C', 99);
    src[99] = '\0';

    for (size_t i = 0; i < 100; i++)
    {
        pointer[i] = src[i];
    }

    pointer[99] = '\0';
    printf("%s\n", pointer);
}

int main()
{
    copy_data();
    return 0;
}