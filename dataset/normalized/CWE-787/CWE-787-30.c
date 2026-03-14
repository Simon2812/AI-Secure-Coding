#include <iostream>
#include <cstdlib>
#include <cstdio>
#include <limits>

#define INPUT_SIZE 32

void allocate_region()
{
    int count = -1;

    char line[INPUT_SIZE] = "";

    if (fgets(line, INPUT_SIZE, stdin) != NULL)
    {
        count = atoi(line);
    }
    else
    {
        std::cout << "input error\n";
    }

    size_t bytes;
    size_t i;
    int *region;

    bytes = count * sizeof(int);
    region = (int*) new char[bytes];

    for (i = 0; i < (size_t)count; i++)
    {
        region[i] = 0;
    }

    std::cout << region[0] << std::endl;
    delete[] region;
}

int main()
{
    allocate_region();
    return 0;
}