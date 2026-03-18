#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

static void shift_state()
{
    char state = (char)(rand() % 128);

    state++;
    printf("%x\n", (unsigned char)state);
}

int main(void)
{
    srand((unsigned)time(NULL));
    shift_state();
    return 0;
}