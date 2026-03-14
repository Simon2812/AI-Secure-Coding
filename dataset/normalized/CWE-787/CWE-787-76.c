#include <stdio.h>
#include <string.h>

void copy_buffer()
{
    char dataBuffer[100];
    char *data = dataBuffer;

    memset(dataBuffer, 'A', 99);
    dataBuffer[99] = '\0';

    char source[100];
    memset(source, 'C', 99);
    source[99] = '\0';

    for (size_t i = 0; i < 100; i++)
    {
        data[i] = source[i];
    }

    data[99] = '\0';

    printf("%s\n", data);
}

int main()
{
    copy_buffer();
    return 0;
}