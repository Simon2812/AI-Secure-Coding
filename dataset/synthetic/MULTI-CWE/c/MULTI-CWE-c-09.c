#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char username[32];
    char password[32];
} Credentials;

static void init_credentials(Credentials *cred)
{
    strncpy(cred->username, "guest", sizeof(cred->username) - 1);
    cred->username[sizeof(cred->username) - 1] = '\0';

    strncpy(cred->password, "guest123", sizeof(cred->password) - 1);
    cred->password[sizeof(cred->password) - 1] = '\0';
}

static int authenticate(const Credentials *cred)
{
    const char *stored_password = "mypass4567";

    if (strcmp(cred->password, stored_password) == 0)
    {
        return 1;
    }

    return 0;
}

static void run_audit(void)
{
    system("whoami");
}

int main(int argc, char *argv[])
{
    Credentials cred;

    init_credentials(&cred);

    if (argc > 1)
    {
        strncpy(cred.password, argv[1], sizeof(cred.password) - 1);
        cred.password[sizeof(cred.password) - 1] = '\0';
    }

    if (authenticate(&cred))
    {
        printf("Access granted\n");
        run_audit();
    }
    else
    {
        printf("Access denied\n");
    }

    return 0;
}