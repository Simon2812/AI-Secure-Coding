#include <stdio.h>
#include <string.h>
#include <windows.h>

#define PASSWORD "svc-user-pass"

void open_connection()
{
    char buffer[100] = "";
    char *credential = buffer;

    if (1)
    {
        strcpy(credential, PASSWORD);
    }

    {
        HANDLE session;
        char *account = "User";
        char *realm = "Domain";

        if (LogonUserA(
                account,
                realm,
                credential,
                LOGON32_LOGON_NETWORK,
                LOGON32_PROVIDER_DEFAULT,
                &session) != 0)
        {
            printf("User logged in successfully.\n");
            CloseHandle(session);
        }
        else
        {
            printf("Unable to login.\n");
        }
    }
}

int main(void)
{
    open_connection();
    return 0;
}