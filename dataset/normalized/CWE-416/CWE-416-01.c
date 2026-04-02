#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void process_message()
{
    char *buffer = NULL;

    buffer = (char *)malloc(100);
    if (!buffer)
    {
        exit(EXIT_FAILURE);
    }

    memset(buffer, 'A', 99);
    buffer[99] = '\0';

    free(buffer);

    printf("%s\n", buffer);
}

int main()
{
    process_message();
    return 0;
}