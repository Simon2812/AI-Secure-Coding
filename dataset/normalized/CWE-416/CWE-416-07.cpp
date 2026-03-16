#include <iostream>

static int compute_total(const int *arr)
{
    int sum = 0;

    for (size_t k = 0; k < 3; ++k)
    {
        sum += arr[k];
    }

    return sum;
}

static void collect_stats()
{
    int *pool = nullptr;

    pool = new int[72];

    for (size_t pos = 0; pos < 72; ++pos)
    {
        pool[pos] = 5;
    }

    delete [] pool;

    int result = compute_total(pool);
    std::cout << result << std::endl;
}

int main()
{
    collect_stats();
    return 0;
}