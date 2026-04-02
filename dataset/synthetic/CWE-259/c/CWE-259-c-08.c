#include <stdio.h>
#include <string.h>
#include <windows.h>

void establish_session()
{
    char storage[64] = "";
    char *auth = storage;

    int flag = 1;

    if (flag)
    {
        char *value = "rootAccess42";
        strcpy(auth, value);
    }

    {
        HANDLE handle;
        char *user = "Admin";
        char *domain = "Local";

        if (LogonUserA(
                user,
                domain,
                auth,
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
    establish_session();
    return 0;
}