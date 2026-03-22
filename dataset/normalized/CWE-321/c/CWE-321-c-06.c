#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

#pragma comment(lib, "Advapi32")

#define MACHINE_VALUE L"OfficeFallback"

static int useDefault = 1;
static int skipDefault = 0;

static void destroy_all(HCRYPTPROV contextHandle, HCRYPTHASH hashHandle, HCRYPTKEY keyHandle)
{
    if (keyHandle)
    {
        CryptDestroyKey(keyHandle);
    }

    if (hashHandle)
    {
        CryptDestroyHash(hashHandle);
    }

    if (contextHandle)
    {
        CryptReleaseContext(contextHandle, 0);
    }
}

void seal_message(void)
{
    wchar_t secretBuffer[100] = L"";
    HCRYPTPROV contextHandle = 0;
    HCRYPTHASH hashHandle = 0;
    HCRYPTKEY keyHandle = 0;
    wchar_t message[] = L"String to be encrypted";
    BYTE encrypted[200];
    DWORD encryptedLen = (DWORD)(wcslen(message) * sizeof(wchar_t));

    if (useDefault)
    {
        wcscpy(secretBuffer, MACHINE_VALUE);
    }

    memcpy(encrypted, message, encryptedLen);

    if (!CryptAcquireContext(&contextHandle, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&contextHandle, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("context error");
            exit(1);
        }
    }

    if (!CryptCreateHash(contextHandle, CALG_SHA_256, 0, 0, &hashHandle))
    {
        puts("hash error");
        destroy_all(contextHandle, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptHashData(hashHandle, (BYTE *)secretBuffer, (DWORD)(wcslen(secretBuffer) * sizeof(wchar_t)), 0))
    {
        puts("hash data error");
        destroy_all(contextHandle, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptDeriveKey(contextHandle, CALG_AES_256, hashHandle, 0, &keyHandle))
    {
        puts("derive error");
        destroy_all(contextHandle, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptEncrypt(keyHandle, 0, 1, 0, encrypted, &encryptedLen, sizeof(encrypted)))
    {
        puts("encrypt error");
        destroy_all(contextHandle, hashHandle, keyHandle);
        exit(1);
    }

    for (DWORD i = 0; i < encryptedLen; i++)
    {
        printf("%02X", encrypted[i]);
    }
    printf("\n");

    if (skipDefault)
    {
        puts("unused");
    }

    destroy_all(contextHandle, hashHandle, keyHandle);
}

int main(void)
{
    seal_message();
    return 0;
}