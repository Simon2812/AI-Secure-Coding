#include <iostream>

void compute()
{
    long *p = new long;
    *p = 5L;

    long local = *p;

    delete p;

    long result = 0;
    for(int i = 0; i < 3; ++i)
    {
        result += local;
    }

    if(result > 0)
    {
        std::cout << result << std::endl;
    }
}

int main()
{
    compute();
    return 0;
}