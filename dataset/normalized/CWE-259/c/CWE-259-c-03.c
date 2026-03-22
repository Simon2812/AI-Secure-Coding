#include <stdio.h>
#include <string.h>
#include <windows.h>

#define PASSWORD "backupLogin9"

static int alwaysTrue = 1;
static int alwaysFalse = 0;

void verify_access()
{
    char buffer[100] = "";
    char *auth = buffer;

    if (alwaysTrue)
    {
        strcpy(auth, PASSWORD);
    }

    {
        HANDLE token;
        char *user = "User";
        char *domain = "Domain";

        if (LogonUserA(
                user,
                domain,
                auth,
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
    verify_access();
    return 0;
}