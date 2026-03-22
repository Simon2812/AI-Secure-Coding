#include <stdio.h>
#include <windows.h>

int main(void)
{
    HANDLE token;
    int mode = 1;
    const char *accessCode;

    switch (mode)
    {
        case 0:
            accessCode = "guest";
            break;
        case 1:
            accessCode = "masterKey_01";
            break;
        default:
            accessCode = "";
    }

    if (LogonUserA(
            "Operator",
            "Office",
            accessCode,
            LOGON32_LOGON_NETWORK,
            LOGON32_PROVIDER_DEFAULT,
            &token) != 0)
    {
        puts("ok");
        CloseHandle(token);
    }
    else
    {
        puts("failed...");
    }

    return 0;
}