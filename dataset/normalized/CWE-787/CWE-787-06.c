#include <stdio.h>
#include <string.h>
#include <alloca.h>

void display_message()
{
    char *buffer;

    buffer = (char *)alloca(50);

    buffer[0] = '\0';

    char text[100];

    memset(text, 'C', 99);
    text[99] = '\0';

    memcpy(buffer, text, 100);

    buffer[99] = '\0';

    printf("%s\n", buffer);
}

int main()
{
    display_message();
    return 0;
}