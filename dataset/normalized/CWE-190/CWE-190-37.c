#include "std_testcase.h"
#include <limits.h>

static void process()
{
    unsigned int value = 0;

    if (fscanf(stdin, "%u", &value) == 1)
    {
        if (value < UINT_MAX)
        {
            value++;
        }

        printUnsignedLine(value);
    }
}

int main(void)
{
    process();
    return 0;
}