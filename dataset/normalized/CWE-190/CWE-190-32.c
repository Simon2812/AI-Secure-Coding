#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

static void transform_byte()
{
    char b = (char)(rand() % 128);

    if (b > 0)
    {
        char out = b;
        if (b <= CHAR_MAX / 3)
        {
            out = b * 3;
        }
        printf("%x\n", (unsigned char)out);
    }
}

int main(void)
{
    srand((unsigned)time(NULL));
    transform_byte();
    return 0;
}