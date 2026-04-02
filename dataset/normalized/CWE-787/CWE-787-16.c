#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void copy_text()
{
    char *buffer;

    buffer = (char *)malloc(4);
    if (buffer == NULL)
    {
        exit(1);
    }

    char text[5] = "TEXT";

    memmove(buffer, text, strlen(text) + 1);

    printf("%s\n", buffer);

    free(buffer);
}

int main()
{
    copy_text();
    return 0;
}