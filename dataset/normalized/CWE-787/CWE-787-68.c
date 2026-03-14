#include <stdio.h>
#include <string.h>

typedef struct
{
    int intOne;
    int intTwo;
} twoIntsStruct;

void copy_records()
{
    twoIntsStruct *buffer;
    twoIntsStruct storage[100];

    buffer = storage;

    twoIntsStruct source[100];

    for (size_t i = 0; i < 100; i++)
    {
        source[i].intOne = 0;
        source[i].intTwo = 0;
    }

    memcpy(buffer, source, 100 * sizeof(twoIntsStruct));

    printf("%d %d\n", buffer[0].intOne, buffer[0].intTwo);
}

int main()
{
    copy_records();
    return 0;
}