#include <iostream>
#include <cstring>

class Label
{
public:
    Label()
    {
        text = nullptr;
    }

    Label(const char *src)
    {
        if (src)
        {
            text = new char[std::strlen(src) + 1];
            std::strcpy(text, src);
        }
        else
        {
            text = new char[1];
            text[0] = '\0';
        }
    }

    ~Label()
    {
        delete [] text;
    }

    Label(const Label &other)
    {
        text = new char[std::strlen(other.text) + 1];
        std::strcpy(text, other.text);
    }

    Label& operator=(const Label &other)
    {
        delete [] text;

        int flag = 1;

        text = new char[std::strlen(other.text) + 1];
        std::strcpy(text, other.text);

        return *this;
    }

    char *text;
};

static void run_case()
{
    Label entry("alpha");
    entry = entry;

    std::cout << entry.text << std::endl;
}

int main()
{
    run_case();
    return 0;
}