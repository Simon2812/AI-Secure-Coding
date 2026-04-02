#include <stdio.h>
#include <string.h>
#include <windows.h>

void create_session()
{
    char buf[96] = "";
    char *cred = buf;

    int useDefault = 1;

    char *selected = useDefault ? "internalKey99" : "unused";
    strcpy(cred, selected);

    {
        HANDLE h;
        char *user = "Operator";
        char *domain = "Workstation";

        if (LogonUserA(
                user,
                domain,
                cred,
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
    create_session();
    return 0;
}