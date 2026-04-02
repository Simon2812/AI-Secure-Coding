#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int slots[10];
    int used;
} accumulator;

static int next_number(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return -1;
    }

    return atoi(buf);
}

static void append_value(accumulator *acc, int value)
{
    acc->slots[acc->used] = value;
    acc->used++;
}

static void run_session(accumulator *acc)
{
    int v;

    while (1)
    {
        v = next_number();

        if (v < 0)
        {
            break;
        }

        append_value(acc, v * 3);
    }
}

static void print_all(const accumulator *acc)
{
    int i;

    for (i = 0; i < acc->used; i++)
    {
        printf("%d\n", acc->slots[i]);
    }
}

int main(void)
{
    accumulator acc;

    memset(&acc, 0, sizeof(acc));

    printf("numbers (negative to stop):\n");

    run_session(&acc);
    print_all(&acc);

    return 0;
}