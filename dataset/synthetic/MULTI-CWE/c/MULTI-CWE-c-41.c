#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char filename[128];
    int limit;
} Input;

static void init_input(Input *in)
{
    strncpy(in->filename, "numbers.txt", sizeof(in->filename) - 1);
    in->filename[sizeof(in->filename) - 1] = '\0';
    in->limit = 10;
}

static void read_args(Input *in, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(in->filename, argv[1], sizeof(in->filename) - 1);
        in->filename[sizeof(in->filename) - 1] = '\0';
    }

    if (argc > 2)
    {
        int v = atoi(argv[2]);
        if (v > 0 && v <= 100)
        {
            in->limit = v;
        }
    }
}

static int load_numbers(const char *file, int *out, int max)
{
    FILE *f = fopen(file, "r");
    int count = 0;

    if (f == NULL)
    {
        return 0;
    }

    while (count < max && fscanf(f, "%d", &out[count]) == 1)
    {
        count++;
    }

    fclose(f);
    return count;
}

static void print_summary(const int *data, int n)
{
    int i;
    int sum = 0;

    for (i = 0; i < n; i++)
    {
        sum += data[i];
    }

    if (n > 0)
    {
        printf("avg: %d\n", sum / n);
    }
}

static void show_file_info(const char *file)
{
    execl("/usr/bin/stat", "stat", file, (char *)NULL);
}

int main(int argc, char *argv[])
{
    Input in;
    int *buffer;
    int count;

    init_input(&in);
    read_args(&in, argc, argv);

    if (in.limit <= 0 || in.limit > 1000)
    {
        return 0;
    }

    buffer = (int *)malloc((size_t)in.limit * sizeof(int));
    if (buffer == NULL)
    {
        return 0;
    }

    count = load_numbers(in.filename, buffer, in.limit);

    print_summary(buffer, count);

    free(buffer);

    show_file_info(in.filename);

    return 0;
}