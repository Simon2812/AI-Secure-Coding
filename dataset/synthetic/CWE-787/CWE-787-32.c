#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void apply_override(const char *path)
{
    FILE *input = fopen(path, "r");
    char text[64];
    int table[6] = {10, 20, 30, 40, 50, 60};
    int target = 0;
    int value = 0;

    if (input == NULL)
    {
        return;
    }

    if (fgets(text, sizeof(text), input) == NULL)
    {
        fclose(input);
        return;
    }

    target = atoi(text);

    if (fgets(text, sizeof(text), input) == NULL)
    {
        fclose(input);
        return;
    }

    value = atoi(text);

    table[target] = value;

    for (target = 0; target < 6; target++)
    {
        printf("%d\n", table[target]);
    }

    fclose(input);
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        return 1;
    }

    apply_override(argv[1]);
    return 0;
}