#include <stdio.h>
#include <wchar.h>
#include <string.h>

void copy_wide_buffer()
{
    wchar_t dataBuffer[100];
    wchar_t *data = dataBuffer;

    wmemset(dataBuffer, L'A', 99);
    dataBuffer[99] = L'\0';

    wchar_t source[100];
    wmemset(source, L'C', 99);
    source[99] = L'\0';

    memmove(data, source, 100 * sizeof(wchar_t));

    data[99] = L'\0';

    wprintf(L"%ls\n", data);
}

int main()
{
    copy_wide_buffer();
    return 0;
}