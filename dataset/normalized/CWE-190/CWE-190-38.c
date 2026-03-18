#include "std_testcase.h"
#include <limits.h>

static void handle()
{
    short value = SHRT_MAX;

    if (value < SHRT_MAX)
    {
        value++;
    }

    printIntLine(value);
}

int main(void)
{
    handle();
    return 0;
}