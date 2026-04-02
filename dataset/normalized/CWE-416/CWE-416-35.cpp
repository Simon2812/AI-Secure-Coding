#include <cwchar>
#include <iostream>
#include <memory>

void process()
{
    std::unique_ptr<wchar_t[]> buffer(new wchar_t[100]);

    std::wmemset(buffer.get(), L'A', 99);
    buffer[99] = L'\0';

    size_t len = std::wcslen(buffer.get());

    wchar_t copy[128];
    std::wmemcpy(copy, buffer.get(), len + 1);

    buffer.reset();

    if(len > 10)
    {
        std::wcout << copy << std::endl;
    }
}

int main()
{
    process();
    return 0;
}