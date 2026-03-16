#include <iostream>
#include <cstring>

static void emit_message()
{
    char *text = nullptr;

    text = new char[96];
    std::memset(text, 'A', 95);
    text[95] = '\0';

    delete [] text;

    std::cout << text << std::endl;
}

int main()
{
    emit_message();
    return 0;
}