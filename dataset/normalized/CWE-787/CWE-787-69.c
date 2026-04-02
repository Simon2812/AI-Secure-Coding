#include <stdio.h>
#include <string.h>
#include <wchar.h>

void copy_text()
{
    char *buffer;
    char dataBuffer[100];

    buffer = dataBuffer;

    memset(buffer, 'A', 49);
    buffer[49] = '\0';

    char destination[50] = "";

    strncpy(destination, buffer, strlen(buffer));

    destination[49] = '\0';

    printf("%s\n", destination);
}

int main()
{
    copy_text();
    return 0;
}