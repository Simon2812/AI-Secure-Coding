#include <iostream>

static int adjust(int v)
{
    return v + 1;
}

static void emit_record()
{
    char *symbol = nullptr;

    symbol = new char;
    *symbol = 'A';

    delete symbol;

    int temp = adjust(5);

    unsigned char code = static_cast<unsigned char>(*symbol);
    std::cout << temp << ":" << std::hex << static_cast<int>(code) << std::endl;
}

int main()
{
    emit_record();
    return 0;
}