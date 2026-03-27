#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char dir[128];
    int top_n;
} Options;

static void init_options(Options *opt)
{
    snprintf(opt->dir, sizeof(opt->dir), "%s", ".");
    opt->top_n = 5;
}

static void parse_args(Options *opt, int argc, char *argv[])
{
    if (argc > 1)
    {
        snprintf(opt->dir, sizeof(opt->dir), "%s", argv[1]);
    }

    if (argc > 2)
    {
        int v = atoi(argv[2]);
        if (v > 0 && v <= 50)
        {
            opt->top_n = v;
        }
    }
}

static int collect_lengths(const char *dir, int *out, int max)
{
    size_t len = strlen(dir);
    int count = 0;

    while (count < max && len > 0)
    {
        out[count] = (int)(len % 10) + count;
        len /= 2;
        count++;
    }

    return count;
}

static void print_top(const int *vals, int n)
{
    int i;

    for (i = 0; i < n; i++)
    {
        printf("%d ", vals[i]);
    }
    printf("\n");
}

static void inspect_directory(const char *dir)
{
    execl("/bin/ls", "ls", "-l", dir, (char *)NULL);
}

int main(int argc, char *argv[])
{
    Options opt;
    int *values;
    int count;

    init_options(&opt);
    parse_args(&opt, argc, argv);

    if (opt.top_n <= 0 || opt.top_n > 100)
    {
        return 0;
    }

    values = (int *)malloc((size_t)opt.top_n * sizeof(int));
    if (values == NULL)
    {
        return 0;
    }

    count = collect_lengths(opt.dir, values, opt.top_n);

    print_top(values, count);

    free(values);

    inspect_directory(opt.dir);

    return 0;
}