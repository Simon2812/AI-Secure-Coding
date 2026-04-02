#include <iostream>
#include <iomanip>

void run()
{
    char *p = new char;
    *p = 'A';

    unsigned char value = static_cast<unsigned char>(*p);

    delete p;

    int transformed = value + 1;

    if(transformed > 0)
    {
        std::cout << std::hex << static_cast<int>(value) << std::endl;
    }
}

int main()
{
    run();
    return 0;
}