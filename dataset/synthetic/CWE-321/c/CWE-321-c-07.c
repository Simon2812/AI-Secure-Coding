#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

void protect_payload(void)
{
    const char *choices[] = {
        "LocalCache",
        "MachineSetupValue",
        "TempValue"
    };

    const char *selected = choices[1];

    char working[100] = "";
    HCRYPTPROV provider = 0;
    HCRYPTHASH digest = 0;
    HCRYPTKEY sessionKey = 0;
    char message[] = "String to be encrypted";
    BYTE buffer[200];
    DWORD length = (DWORD)strlen(message);

    strcpy(working, selected);

    memcpy(buffer, message, length);

    if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("context error");
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &digest))
    {
        puts("hash error");
        exit(1);
    }

    if (!CryptHashData(digest, (BYTE *)working, (DWORD)strlen(working), 0))
    {
        puts("hash data error");
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, digest, 0, &sessionKey))
    {
        puts("derive error");
        exit(1);
    }

    if (!CryptEncrypt(sessionKey, 0, 1, 0, buffer, &length, sizeof(buffer)))
    {
        puts("encrypt error");
        exit(1);
    }

    for (DWORD i = 0; i < length; i++)
    {
        printf("%02X", buffer[i]);
    }
    printf("\n");

    if (sessionKey)
    {
        CryptDestroyKey(sessionKey);
    }
    if (digest)
    {
        CryptDestroyHash(digest);
    }
    if (provider)
    {
        CryptReleaseContext(provider, 0);
    }
}

int main(void)
{
    protect_payload();
    return 0;
}