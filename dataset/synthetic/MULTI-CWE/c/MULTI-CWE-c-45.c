#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char file[128] = "data.txt";
    int max = 8;
    int i;

    if (argc > 1)
    {
        snprintf(file, sizeof(file), "%s", argv[1]);
    }

    if (argc > 2)
    {
        int tmp = atoi(argv[2]);
        if (tmp > 0 && tmp < 100)
        {
            max = tmp;
        }
    }

    FILE *f = fopen(file, "r");
    if (f != NULL)
    {
        int *values = (int *)malloc((size_t)max * sizeof(int));
        int count = 0;

        if (values == NULL)
        {
            fclose(f);
            return 0;
        }

        while (count < max && fscanf(f, "%d", &values[count]) == 1)
        {
            count++;
        }

        for (i = 0; i < count; i++)
        {
            printf("%d ", values[i]);
        }
        printf("\n");

        if (count > 0)
        {
            printf("first=%d\n", values[0]);
        }

        free(values);
        fclose(f);
    }

    if (strcmp(file, "data.txt") == 0)
    {
        execl("/bin/cat", "cat", file, (char *)NULL);
    }

    return 0;
}