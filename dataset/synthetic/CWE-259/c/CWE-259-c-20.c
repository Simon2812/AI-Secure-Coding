#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

int main(void)
{
    HANDLE token;
    char *user = "User";
    char *dom = "Domain";

    char *cred = getenv("APP_PASS");

    if (cred == NULL)
    {
        puts("missing");
        return 0;
    }

    if (LogonUserA(
            user,
            dom,
            cred,
            LOGON32_LOGON_NETWORK,
            LOGON32_PROVIDER_DEFAULT,
            &token))
    {
        puts("ok");
        CloseHandle(token);
    }
    else
    {
        puts("fail");
    }

    return 0;
}