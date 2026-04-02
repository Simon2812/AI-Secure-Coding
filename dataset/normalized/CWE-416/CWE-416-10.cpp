#include <iostream>

class Entry
{
public:
    int a;
    int b;
};

static int extract_value(const Entry *e)
{
    return e->a;
}

static void dispatch_frame()
{
    Entry *item = nullptr;

    item = new Entry;
    item->a = 1;
    item->b = 2;

    delete item;

    int value = extract_value(item);
    std::cout << value << std::endl;
}

int main()
{
    dispatch_frame();
    return 0;
}