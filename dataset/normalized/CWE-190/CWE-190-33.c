#include <stdio.h>
#include <limits.h>

static void read_and_shift()
{
    char ch = 0;

    if (fscanf(stdin, "%c", &ch) != 1)
    {
        return;
    }

    char next = ch;
    if (ch < CHAR_MAX)
    {
        next = ch + 1;
    }

    printf("%x\n", (unsigned char)next);
}

int main(void)
{
    read_and_shift();
    return 0;
}