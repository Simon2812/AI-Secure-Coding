#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void copy_block()
{
    char *ptr = NULL;

    char *block = (char *)malloc(10);
    if (block == NULL) exit(1);

    memset(block, 'A', 9);
    block[9] = '\0';

    ptr = block - 15;

    char src[10];
    memset(src, 'C', 9);
    src[9] = '\0';

    strncpy(ptr, src, 9);
    ptr[9] = '\0';

    printf("%s\n", ptr);
}

int main()
{
    copy_block();
    return 0;
}