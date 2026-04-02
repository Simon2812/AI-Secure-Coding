#include <cstring>
#include <iostream>

class Holder
{
public:
    Holder()
    {
        text = nullptr;
    }

    Holder(const char *s)
    {
        if (s)
        {
            size_t n = std::strlen(s);
            text = new char[n + 1];
            std::memcpy(text, s, n + 1);
        }
        else
        {
            text = new char[1];
            text[0] = '\0';
        }
    }

    ~Holder()
    {
        delete [] text;
    }

    Holder(const Holder &other)
    {
        size_t n = std::strlen(other.text);
        text = new char[n + 1];
        std::memcpy(text, other.text, n + 1);
    }

    Holder& operator=(const Holder &other)
    {
        if (this != &other)
        {
            char *tmp = new char[std::strlen(other.text) + 1];
            std::strcpy(tmp, other.text);

            delete [] text;
            text = tmp;
        }
        return *this;
    }

    char *text;
};

void execute()
{
    Holder a("example");
    Holder b;

    b = a;

    std::cout << b.text << std::endl;
}

int main()
{
    execute();
    return 0;
}