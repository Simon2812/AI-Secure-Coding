#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

static void release_all(HCRYPTPROV provider, HCRYPTHASH hashObj, HCRYPTKEY keyObj)
{
    if (keyObj)
    {
        CryptDestroyKey(keyObj);
    }
    if (hashObj)
    {
        CryptDestroyHash(hashObj);
    }
    if (provider)
    {
        CryptReleaseContext(provider, 0);
    }
}

void seal_entry(void)
{
    char runtimeValue[100] = "";
    char *env = getenv("APP_SECRET");

    if (env != NULL)
    {
        strncpy(runtimeValue, env, sizeof(runtimeValue) - 1);
        runtimeValue[sizeof(runtimeValue) - 1] = '\0';
    }

    HCRYPTPROV provider = 0;
    HCRYPTKEY sessionKey = 0;
    HCRYPTHASH hashObj = 0;

    char record[] = "user note";
    DWORD len = (DWORD)strlen(record);
    BYTE out[200];

    memcpy(out, record, len);

    if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("acquire error");
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hashObj))
    {
        puts("hash error");
        release_all(provider, hashObj, sessionKey);
        exit(1);
    }

    if (!CryptHashData(hashObj, (BYTE *)runtimeValue, (DWORD)strlen(runtimeValue), 0))
    {
        puts("hash data error");
        release_all(provider, hashObj, sessionKey);
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, hashObj, 0, &sessionKey))
    {
        puts("derive error");
        release_all(provider, hashObj, sessionKey);
        exit(1);
    }

    if (!CryptEncrypt(sessionKey, 0, 1, 0, out, &len, sizeof(out)))
    {
        puts("encrypt error");
        release_all(provider, hashObj, sessionKey);
        exit(1);
    }

    for (DWORD i = 0; i < len; i++)
    {
        printf("%02X", out[i]);
    }
    printf("\n");

    release_all(provider, hashObj, sessionKey);
}

int main(void)
{
    seal_entry();
    return 0;
}