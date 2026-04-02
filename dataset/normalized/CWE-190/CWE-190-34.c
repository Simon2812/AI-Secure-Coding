#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

static void square_byte()
{
    char v = (char)(rand() % 128);

    char out = 0;
    if (v != 0 && v <= CHAR_MAX / v)
    {
        out = v * v;
    }

    printf("%x\n", (unsigned char)out);
}

int main(void)
{
    srand((unsigned)time(NULL));
    square_byte();
    return 0;
}