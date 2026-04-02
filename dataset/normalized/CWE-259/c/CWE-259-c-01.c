#include <stdio.h>
#include <string.h>
#include <windows.h>

#define PASSWORD "internalAuth42"

void start_session()
{
    char buffer[100] = "";
    char *secret = buffer;

    strcpy(secret, PASSWORD);

    {
        HANDLE handle;
        char *user = "User";
        char *domain = "Domain";

        if (LogonUserA(
                user,
                domain,
                secret,
                LOGON32_LOGON_NETWORK,
                LOGON32_PROVIDER_DEFAULT,
                &handle) != 0)
        {
            printf("User logged in successfully.\n");
            CloseHandle(handle);
        }
        else
        {
            printf("Unable to login.\n");
        }
    }
}

int main(void)
{
    start_session();
    return 0;
}