#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

#pragma comment(lib, "Advapi32")

#define SYSTEM_PHRASE L"TenantWideValue"

static void release_state(HCRYPTPROV provider, HCRYPTHASH hashValue, HCRYPTKEY sessionKey)
{
    if (sessionKey)
    {
        CryptDestroyKey(sessionKey);
    }

    if (hashValue)
    {
        CryptDestroyHash(hashValue);
    }

    if (provider)
    {
        CryptReleaseContext(provider, 0);
    }
}

void lock_text(void)
{
    wchar_t seedText[100] = L"";
    HCRYPTPROV provider = 0;
    HCRYPTHASH hashValue = 0;
    HCRYPTKEY sessionKey = 0;
    wchar_t text[] = L"String to be encrypted";
    BYTE output[200];
    DWORD outputLen = (DWORD)(wcslen(text) * sizeof(wchar_t));

    if (5 == 5)
    {
        wcscpy(seedText, SYSTEM_PHRASE);
    }

    memcpy(output, text, outputLen);

    if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("context error");
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hashValue))
    {
        puts("hash error");
        release_state(provider, hashValue, sessionKey);
        exit(1);
    }

    if (!CryptHashData(hashValue, (BYTE *)seedText, (DWORD)(wcslen(seedText) * sizeof(wchar_t)), 0))
    {
        puts("hash data error");
        release_state(provider, hashValue, sessionKey);
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, hashValue, 0, &sessionKey))
    {
        puts("derive error");
        release_state(provider, hashValue, sessionKey);
        exit(1);
    }

    if (!CryptEncrypt(sessionKey, 0, 1, 0, output, &outputLen, sizeof(output)))
    {
        puts("encrypt error");
        release_state(provider, hashValue, sessionKey);
        exit(1);
    }

    for (DWORD i = 0; i < outputLen; i++)
    {
        printf("%02X", output[i]);
    }
    printf("\n");

    release_state(provider, hashValue, sessionKey);
}

int main(void)
{
    lock_text();
    return 0;
}