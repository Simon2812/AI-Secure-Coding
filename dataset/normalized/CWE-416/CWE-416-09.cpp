#include <iostream>
#include <cwchar>

static void output_text(const wchar_t *text)
{
    std::wcout << text << std::endl;
}

static void render_item()
{
    wchar_t *content = nullptr;

    content = new wchar_t[80];
    std::wmemset(content, L'A', 79);
    content[79] = L'\0';

    delete [] content;

    output_text(content);
}

int main()
{
    render_item();
    return 0;
}