#include <stdio.h>
#include <string.h>
#include <alloca.h>
#include <wchar.h>

void copy_block()
{
    char *buffer;
    char *workspace = (char *)alloca(1000 * sizeof(char));

    buffer = workspace;
    buffer[0] = '\0';

    char source[1000];

    memset(source, 'C', 999);
    source[999] = '\0';

    memcpy(buffer, source, 1000 * sizeof(char));

    buffer[999] = '\0';

    printf("%s\n", buffer);
}

int main()
{
    copy_block();
    return 0;
}