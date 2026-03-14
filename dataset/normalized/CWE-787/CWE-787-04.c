#include <stdio.h>
#include <string.h>
#include <alloca.h>

void handle_text()
{
    char *buffer;

    buffer = (char *)alloca(10 * sizeof(char));
    buffer[0] = '\0';

    char input[11] = "TenLetters";

    strcpy(buffer, input);

    printf("%s\n", buffer);
}

int main()
{
    handle_text();
    return 0;
}