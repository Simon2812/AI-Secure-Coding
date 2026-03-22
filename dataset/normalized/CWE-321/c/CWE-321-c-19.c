#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

#pragma comment(lib, "Advapi32")

static const int useEnvironment = 1;
static const int skipUnusedPath = 0;

static void close_crypto(HCRYPTPROV provider, HCRYPTHASH hashHandle, HCRYPTKEY keyHandle)
{
    if (keyHandle)
    {
        CryptDestroyKey(keyHandle);
    }

    if (hashHandle)
    {
        CryptDestroyHash(hashHandle);
    }

    if (provider)
    {
        CryptReleaseContext(provider, 0);
    }
}

void protect_note(void)
{
    wchar_t keyBuffer[100] = L"";
    HCRYPTPROV provider = 0;
    HCRYPTKEY keyHandle = 0;
    HCRYPTHASH hashHandle = 0;
    wchar_t message[] = L"Monthly summary";
    DWORD dataLen = (DWORD)(wcslen(message) * sizeof(wchar_t));
    BYTE encrypted[200];

    if (useEnvironment)
    {
        wchar_t *envValue = _wgetenv(L"APP_SECRET");
        if (envValue != NULL)
        {
            wcsncpy(keyBuffer, envValue, 99);
            keyBuffer[99] = L'\0';
        }
    }

    if (skipUnusedPath)
    {
        wcscpy(keyBuffer, L"unused");
    }

    memcpy(encrypted, message, dataLen);

    if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("Error in acquiring cryptographic context");
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hashHandle))
    {
        puts("Error in creating hash");
        close_crypto(provider, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptHashData(hashHandle, (BYTE *)keyBuffer, (DWORD)(wcslen(keyBuffer) * sizeof(wchar_t)), 0))
    {
        puts("Error in hashing key input");
        close_crypto(provider, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, hashHandle, 0, &keyHandle))
    {
        puts("Error in CryptDeriveKey");
        close_crypto(provider, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptEncrypt(keyHandle, (HCRYPTHASH)NULL, 1, 0, encrypted, &dataLen, sizeof(encrypted)))
    {
        puts("Error in CryptEncrypt");
        close_crypto(provider, hashHandle, keyHandle);
        exit(1);
    }

    for (DWORD i = 0; i < dataLen; i++)
    {
        printf("%02X", encrypted[i]);
    }
    printf("\n");

    close_crypto(provider, hashHandle, keyHandle);
}

int main(void)
{
    protect_note();
    return 0;
}
