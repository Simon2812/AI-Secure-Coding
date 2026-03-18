#include <stdio.h>
#include <limits.h>

static void advance_level()
{
    char level = CHAR_MAX;

    char next = level + 1;
    printf("%x\n", (unsigned char)next);
}

int main(void)
{
    advance_level();
    return 0;
}