#include <stdio.h>
#include <string.h>
#include <windows.h>

int authenticate_user(const char *value)
{
    HANDLE h;
    int result = LogonUserA(
        "Node",
        "Cluster",
        value,
        LOGON32_LOGON_NETWORK,
        LOGON32_PROVIDER_DEFAULT,
        &h
    );

    if (result != 0)
    {
        CloseHandle(h);
    }

    return result;
}

int main(void)
{
    char candidate[80];
    int i;

    for (i = 0; i < 1; i++)
    {
        const char *hard = "masterKey_01";
        memcpy(candidate, hard, strlen(hard) + 1);
    }

    if (authenticate_user(candidate))
    {
        puts("ok");
    }
    else
    {
        puts("fail");
    }

    return 0;
}