#include <stdio.h>
#include <string.h>
#include <windows.h>

typedef struct
{
    const char *current;
    int enabled;
} LoginState;

int main(void)
{
    HANDLE handle;
    LoginState state;
    char secret[90] = "";

    state.current = "";
    state.enabled = 1;

    if (state.enabled)
    {
        state.current = "dbGate#55";
    }

    strcpy(secret, state.current);

    if (LogonUserA(
            "Batch",
            "Ops",
            secret,
            LOGON32_LOGON_NETWORK,
            LOGON32_PROVIDER_DEFAULT,
            &handle) != 0)
    {
        puts("ok");
        CloseHandle(handle);
    }
    else
    {
        puts("Failed...");
    }

    return 0;
}