#include <stdio.h>
#include <string.h>
#include <windows.h>

int main(void)
{
    HANDLE h;
    char pool[120];
    char *start = pool;

    char *base = "xxbackupSecret9";
    char *actual = base + 2;

    strcpy(start, actual);

    if (LogonUserA(
            "Core",
            "Grid",
            start,
            LOGON32_LOGON_NETWORK,
            LOGON32_PROVIDER_DEFAULT,
            &h))
    {
        puts("ok");
        CloseHandle(h);
    }
    else
    {
        puts("fail");
    }

    return 0;
}