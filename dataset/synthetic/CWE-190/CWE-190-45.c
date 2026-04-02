#include <stdio.h>
#include <limits.h>

static int normalize(int value)
{
    if (value % 2 == 0)
        return value;
    return value - 1;
}

static int compute_area(int w, int h)
{
    int width = normalize(w);
    int height = normalize(h);

    int area = width * height;

    return area;
}

int main(void)
{
    int rawWidth = 32000;
    int rawHeight = 24000;

    int adjustedWidth = rawWidth - 1000;
    int adjustedHeight = rawHeight - 1000;

    int size = compute_area(adjustedWidth, adjustedHeight);

    if (size > 1000000)
        printf("%d\n", size);
    else
        puts("small");

    return 0;
}