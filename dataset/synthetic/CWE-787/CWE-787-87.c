#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int cells[20];
} field;

static int read_stride(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 1;
    }

    return atoi(line);
}

static void apply_pattern(field *f, int stride)
{
    int i;
    int position = 0;

    if (stride <= 0)
    {
        return;
    }

    for (i = 0; i < 20 && position < 20; i++)
    {
        f->cells[position] = i * 9;
        position += stride;
    }
}

static void print_field(const field *f)
{
    int i;

    for (i = 0; i < 20; i++)
    {
        printf("%d\n", f->cells[i]);
    }
}

int main(void)
{
    field f;
    int stride;

    memset(&f, 0, sizeof(f));

    printf("stride:\n");
    stride = read_stride();

    apply_pattern(&f, stride);
    print_field(&f);

    return 0;
}