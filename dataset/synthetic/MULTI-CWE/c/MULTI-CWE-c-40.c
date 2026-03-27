#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char directory[128];
    int amount;
} Settings;

static void init(Settings *s)
{
    strncpy(s->directory, ".", sizeof(s->directory) - 1);
    s->directory[sizeof(s->directory) - 1] = '\0';
    s->amount = 4;
}

static void read_input(Settings *s, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(s->directory, argv[1], sizeof(s->directory) - 1);
        s->directory[sizeof(s->directory) - 1] = '\0';
    }

    if (argc > 2)
    {
        int v = atoi(argv[2]);
        if (v > 0 && v < 100)
        {
            s->amount = v;
        }
    }
}

static void list_dir(const char *dir)
{
    execl("/bin/ls", "ls", "-1", dir, (char *)NULL);
}

static void compute_series(int n)
{
    int *vals;
    int i;

    if (n <= 0 || n > 100)
    {
        return;
    }

    vals = (int *)malloc((size_t)n * sizeof(int));
    if (vals == NULL)
    {
        return;
    }

    for (i = 0; i < n; i++)
    {
        vals[i] = i * i;
    }

    printf("last: %d\n", vals[n - 1]);

    free(vals);
}

int main(int argc, char *argv[])
{
    Settings s;

    init(&s);
    read_input(&s, argc, argv);

    compute_series(s.amount);
    list_dir(s.directory);

    return 0;
}