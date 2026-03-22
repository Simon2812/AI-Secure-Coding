#include <stdio.h>
#include <string.h>
#include <windows.h>

static void fill_value(char *dst)
{
    char *data = "loginToken77";
    strcpy(dst, data);
}

void run_auth()
{
    char local[80] = "";
    char *token = local;

    fill_value(token);

    {
        HANDLE h;
        char *user = "Service";
        char *domain = "Corp";

        if (LogonUserA(
                user,
                domain,
                token,
                LOGON32_LOGON_NETWORK,
                LOGON32_PROVIDER_DEFAULT,
                &h) != 0)
        {
            printf("User logged in successfully.\n");
            CloseHandle(h);
        }
        else
        {
            printf("Unable to login.\n");
        }
    }
}

int main(void)
{
    run_auth();
    return 0;
}