#include <stdio.h>
#include <wchar.h>
#include <string.h>
#include <alloca.h>

void move_wchars()
{
    wchar_t *ptr;

    wchar_t *buffer = (wchar_t *)alloca(100 * sizeof(wchar_t));
    wmemset(buffer, L'A', 99);
    buffer[99] = L'\0';

    ptr = buffer - 5;

    wchar_t src[100];
    wmemset(src, L'C', 99);
    src[99] = L'\0';

    memmove(ptr, src, 100 * sizeof(wchar_t));

    ptr[99] = L'\0';

    wprintf(L"%ls\n", ptr);
}

int main()
{
    move_wchars();
    return 0;
}