#include <stdio.h>
#include <string.h>
#include <alloca.h>

void copy_text()
{
    char *input;
    char *space = (char *)alloca(100);

    input = space;

    memset(input, 'A', 99);
    input[99] = '\0';

    char out[50] = "";

    size_t len = strlen(input);

    for (size_t i = 0; i < len; i++)
    {
        out[i] = input[i];
    }

    out[49] = '\0';

    printf("%s\n", input);
}

int main()
{
    copy_text();
    return 0;
}