#include <iostream>
#include <cstdlib>
#include <cstring>
#include <limits>

#define INPUT_SIZE 32

void allocate_array()
{
    char inputBuffer[INPUT_SIZE];
    int count = 0;

    if (fgets(inputBuffer, INPUT_SIZE, stdin) == NULL)
    {
        std::cout << "input failed\n";
        return;
    }

    count = atoi(inputBuffer);

    if (count <= 0)
    {
        std::cout << "invalid size\n";
        return;
    }

    if ((size_t)count > SIZE_MAX / sizeof(int))
    {
        std::cout << "size overflow detected\n";
        return;
    }

    size_t bytes = (size_t)count * sizeof(int);

    int *buffer = reinterpret_cast<int*>(new char[bytes]);

    for (size_t i = 0; i < (size_t)count; i++)
    {
        buffer[i] = 0;
    }

    std::cout << buffer[0] << std::endl;

    delete[] reinterpret_cast<char*>(buffer);
}

int main()
{
    allocate_array();
    return 0;
}
