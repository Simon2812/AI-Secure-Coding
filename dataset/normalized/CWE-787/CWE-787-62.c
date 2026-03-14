#include <stdio.h>
#include <string.h>

void copy_text()
{
    char source[100];
    char destination[50];

    memset(source, 'A', 49);
    source[49] = '\0';

    strncpy(destination, source, sizeof(destination) - 1);
    destination[sizeof(destination) - 1] = '\0';

    printf("%s\n", destination);
}

int main()
{
    copy_text();
    return 0;
}