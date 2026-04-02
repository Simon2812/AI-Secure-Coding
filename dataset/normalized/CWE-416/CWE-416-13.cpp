#include <iostream>

struct Pair {
    int first;
    int second;
};

static void report_pair(const Pair *p)
{
    std::cout << p->first << "," << p->second << std::endl;
}

static void handle_pair()
{
    Pair *node = nullptr;

    node = new Pair;
    node->first = 1;
    node->second = 2;

    delete node;

    int marker = 10;

    report_pair(node);
}

int main()
{
    handle_pair();
    return 0;
}