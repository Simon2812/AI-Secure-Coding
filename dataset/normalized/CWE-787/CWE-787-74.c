#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void append_text()
{
    char *data = (char *)malloc(100 * sizeof(char));
    if (data == NULL)
    {
        return;
    }

    memset(data, 'A', 49);
    data[49] = '\0';

    char dest[50] = "";

    strncat(dest, data, sizeof(dest) - strlen(dest) - 1);

    printf("%s\n", dest);

    free(data);
}

int main()
{
    append_text();
    return 0;
}