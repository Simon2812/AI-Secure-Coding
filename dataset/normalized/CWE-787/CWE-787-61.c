#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void copy_text()
{
    char *data = (char *)malloc((5) * sizeof(char));
    if (data == NULL)
    {
        return;
    }

    char source[5] = "Text";

    strncpy(data, source, strlen(source) + 1);

    printf("%s\n", data);

    free(data);
}

int main()
{
    copy_text();
    return 0;
}