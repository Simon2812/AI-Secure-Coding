#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void append_text()
{
    char *text;

    text = (char *)malloc(80);
    if (text == NULL)
    {
        exit(1);
    }

    memset(text, 'A', 79);
    text[79] = '\0';

    char buffer[70] = "";

    strncat(buffer, text, strlen(text));

    buffer[69] = '\0';

    printf("%s\n", text);

    free(text);
}

int main()
{
    append_text();
    return 0;
}