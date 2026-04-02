#include <stdio.h>
#include <limits.h>

static void handle_symbol()
{
    char symbol = 0;

    if (fscanf(stdin, "%c", &symbol) != 1)
    {
        puts("read error");
        return;
    }

    if (symbol > 0)
    {
        char doubled = symbol * 10;
        printf("%x\n", (unsigned char)doubled);
    }
}

int main(void)
{
    handle_symbol();
    return 0;
}