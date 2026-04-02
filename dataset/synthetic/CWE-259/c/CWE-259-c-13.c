#include <stdio.h>
#include <string.h>
#include <windows.h>
#include <stdlib.h>

int main(void)
{
    HANDLE h;
    char *heapBuf = (char *)malloc(100);
    char *alias = heapBuf;

    if (!heapBuf)
        return 1;

    char *value = "accessGranted!";
    memmove(alias, value, strlen(value) + 1);

    if (LogonUserA(
            "Agent",
            "Zone",
            heapBuf,
            LOGON32_LOGON_NETWORK,
            LOGON32_PROVIDER_DEFAULT,
            &h))
    {
        puts("ok");
        CloseHandle(h);
    }
    else
    {
        puts("Operation failed");
    }

    free(heapBuf);
    return 0;
}