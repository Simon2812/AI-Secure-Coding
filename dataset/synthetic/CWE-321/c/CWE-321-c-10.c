#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

static const char *select_value(int mode)
{
    if (mode == 1)
    {
        return "DefaultValue";
    }
    return "";
}

void process_data(void)
{
    char buffer[100] = "";
    HCRYPTPROV provider = 0;
    HCRYPTHASH hash = 0;
    HCRYPTKEY key = 0;

    char input[] = "String to be encrypted";
    BYTE output[200];
    DWORD outputLen = (DWORD)strlen(input);

    const char *chosen = select_value(1);
    strcpy(buffer, chosen);

    memcpy(output, input, outputLen);

    if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("context error");
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hash))
    {
        puts("hash error");
        exit(1);
    }

    if (!CryptHashData(hash, (BYTE *)buffer, (DWORD)strlen(buffer), 0))
    {
        puts("hash data error");
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, hash, 0, &key))
    {
        puts("derive error");
        exit(1);
    }

    if (!CryptEncrypt(key, 0, 1, 0, output, &outputLen, sizeof(output)))
    {
        puts("encrypt error");
        exit(1);
    }

    for (DWORD i = 0; i < outputLen; i++)
    {
        printf("%02X", output[i]);
    }
    printf("\n");

    if (key) CryptDestroyKey(key);
    if (hash) CryptDestroyHash(hash);
    if (provider) CryptReleaseContext(provider, 0);
}

int main(void)
{
    process_data();
    return 0;
}