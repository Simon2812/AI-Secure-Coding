#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *tag;
    int id;
} Node;

int main(void)
{
    Node items[3];

    for (int i = 0; i < 3; i++)
    {
        items[i].tag = (char *)malloc(16);
        if (!items[i].tag)
            return 1;

        snprintf(items[i].tag, 16, "item_%d", i);
        items[i].id = i * 10;
    }

    int checksum = 0;

    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; items[i].tag[j] != '\0'; j++)
            checksum += items[i].tag[j];

        checksum += items[i].id;
    }

    printf("%d\n", checksum);

    return checksum % 3;
}