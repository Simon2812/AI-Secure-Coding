#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void duplicate_text()
{
    char *buf;

    buf = (char *)malloc(5);
    if (buf == NULL)
    {
        exit(1);
    }

    char text[6] = "Hello";

    strncpy(buf, text, strlen(text) + 1);

    printf("%s\n", buf);

    free(buf);
}

int main()
{
    duplicate_text();
    return 0;
}