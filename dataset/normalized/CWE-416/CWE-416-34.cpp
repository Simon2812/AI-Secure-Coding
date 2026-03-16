#include <iostream>
#include <vector>

struct Item
{
    int intOne;
    int intTwo;
};

void run()
{
    std::vector<Item> storage;
    storage.resize(100);

    for (size_t i = 0; i < storage.size(); ++i)
    {
        storage[i].intOne = 1;
        storage[i].intTwo = 2;
    }

    int accumulator = 0;

    for (size_t j = 0; j < 20; ++j)
    {
        accumulator += storage[j].intOne;
    }

    std::vector<Item> temp;
    temp.swap(storage);

    int tail = 0;
    for (size_t k = 0; k < 5; ++k)
    {
        tail += temp[k].intTwo;
    }

    temp.clear();

    int result = accumulator + tail;

    if (result > 0)
    {
        std::cout << result << std::endl;
    }
}
z
int main()
{
    run();
    return 0;
}