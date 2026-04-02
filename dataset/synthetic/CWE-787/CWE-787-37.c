#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int samples[6];
} meter;

static void load_samples(meter *m)
{
    char input[128];
    int i = 0;
    int count = 0;

    if (fgets(input, sizeof(input), stdin) == NULL)
    {
        return;
    }

    count = atoi(input);

    for (i = 0; i < count; i++)
    {
        if (fgets(input, sizeof(input), stdin) == NULL)
        {
            break;
        }

        m->samples[i] = atoi(input);
    }
}

static void display(const meter *m)
{
    int i;

    for (i = 0; i < 6; i++)
    {
        printf("%d\n", m->samples[i]);
    }
}

int main(void)
{
    meter m;
    memset(&m, 0, sizeof(m));

    load_samples(&m);
    display(&m);

    return 0;
}