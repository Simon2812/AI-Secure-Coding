#include <iostream>

struct Pair {
    int x;
    int y;
};

static void log_pair(const Pair *p)
{
    std::cout << p->x << " " << p->y << std::endl;
}

static void publish_batch()
{
    Pair *records = nullptr;

    records = new Pair[48];

    for (size_t n = 0; n < 48; ++n)
    {
        records[n].x = 1;
        records[n].y = 2;
    }

    delete [] records;

    log_pair(&records[0]);
}

int main()
{
    publish_batch();
    return 0;
}