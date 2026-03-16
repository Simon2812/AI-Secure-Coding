#include <iostream>
#include <cstdint>

static void summarize_batch()
{
    int64_t *entries = nullptr;
    size_t idx;

    entries = new int64_t[64];

    for (idx = 0; idx < 64; idx++)
    {
        entries[idx] = 5LL;
    }

    delete [] entries;

    int64_t first = entries[0];
    std::cout << first << std::endl;
}

int main()
{
    summarize_batch();
    return 0;
}