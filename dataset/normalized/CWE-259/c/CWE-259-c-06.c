#include <stdio.h>
#include <wchar.h>
#include <windows.h>

#define PASSWORD L"rootAccess!"

static int flagTrue = 1;
static int flagFalse = 0;

void connect_service()
{
    wchar_t buffer[100] = L"";
    wchar_t *cred = buffer;

    if (flagTrue)
    {
        wcscpy(cred, PASSWORD);
    }

    {
        HANDLE token;
        wchar_t *user = L"User";
        wchar_t *domain = L"Domain";

        if (LogonUserW(
                user,
                domain,
                cred,
                LOGON32_LOGON_NETWORK,
                LOGON32_PROVIDER_DEFAULT,
                &token) != 0)
        {
            printf("User logged in successfully.\n");
            CloseHandle(token);
        }
        else
        {
            printf("Unable to login.\n");
        }
    }
}

int main(void)
{
    connect_service();
    return 0;
}