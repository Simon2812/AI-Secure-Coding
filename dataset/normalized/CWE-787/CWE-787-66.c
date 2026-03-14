#include <stdio.h>
#include <string.h>
#include <alloca.h>
#include <wchar.h>

#define SRC_STRING "HELLO"

void copy_string()
{
    char *buffer;

    buffer = (char *)alloca((6) * sizeof(char));
    buffer[0] = '\0';

    char source[6] = SRC_STRING;

    strcpy(buffer, source);

    printf("%s\n", buffer);
}

int main()
{
    copy_string();
    return 0;
}