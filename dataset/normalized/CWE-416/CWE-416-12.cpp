#include <iostream>

static long scale(long v)
{
    return v * 3;
}

static void process_entry()
{
    long *entry = nullptr;

    entry = new long;
    *entry = 5L;

    delete entry;

    long adjusted = scale(2);

    long result = *entry;
    std::cout << adjusted << ":" << result << std::endl;
}

int main()
{
    process_entry();
    return 0;
}