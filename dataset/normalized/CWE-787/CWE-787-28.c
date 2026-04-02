#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int RAND32()
{
    return rand();
}

void build_array()
{
    int amount = -1;

    amount = RAND32();

    size_t i;
    int *workspace;

    workspace = (int *)malloc(amount * sizeof(int));
    if (workspace == NULL) exit(1);

    for (i = 0; i < (size_t)amount; i++)
    {
        workspace[i] = 0;
    }

    printf("%d\n", workspace[0]);
    free(workspace);
}

int main()
{
    srand((unsigned)time(NULL));
    build_array();
    return 0;
}