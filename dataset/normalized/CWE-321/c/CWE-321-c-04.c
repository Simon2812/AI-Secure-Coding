#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

#pragma comment(lib, "Advapi32")

#define FALLBACK_PHRASE L"StageWideSecret"

static void close_handles(HCRYPTPROV providerHandle, HCRYPTHASH hashHandle, HCRYPTKEY derivedHandle)
{
    if (derivedHandle)
    {
        CryptDestroyKey(derivedHandle);
    }

    if (hashHandle)
    {
        CryptDestroyHash(hashHandle);
    }

    if (providerHandle)
    {
        CryptReleaseContext(providerHandle, 0);
    }
}

void encode_record(void)
{
    wchar_t secretText[100] = L"";
    HCRYPTPROV providerHandle = 0;
    HCRYPTHASH hashHandle = 0;
    HCRYPTKEY derivedHandle = 0;
    wchar_t plainText[] = L"String to be encrypted";
    BYTE cipherText[200];
    DWORD cipherLen = (DWORD)(wcslen(plainText) * sizeof(wchar_t));

    wcscpy(secretText, FALLBACK_PHRASE);

    memcpy(cipherText, plainText, cipherLen);

    if (!CryptAcquireContext(&providerHandle, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&providerHandle, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("context error");
            exit(1);
        }
    }

    if (!CryptCreateHash(providerHandle, CALG_SHA_256, 0, 0, &hashHandle))
    {
        puts("hash error");
        close_handles(providerHandle, hashHandle, derivedHandle);
        exit(1);
    }

    if (!CryptHashData(hashHandle, (BYTE *)secretText, (DWORD)(wcslen(secretText) * sizeof(wchar_t)), 0))
    {
        puts("hash data error");
        close_handles(providerHandle, hashHandle, derivedHandle);
        exit(1);
    }

    if (!CryptDeriveKey(providerHandle, CALG_AES_256, hashHandle, 0, &derivedHandle))
    {
        puts("derive error");
        close_handles(providerHandle, hashHandle, derivedHandle);
        exit(1);
    }

    if (!CryptEncrypt(derivedHandle, 0, 1, 0, cipherText, &cipherLen, sizeof(cipherText)))
    {
        puts("encrypt error");
        close_handles(providerHandle, hashHandle, derivedHandle);
        exit(1);
    }

    for (DWORD i = 0; i < cipherLen; i++)
    {
        printf("%02X", cipherText[i]);
    }
    printf("\n");

    close_handles(providerHandle, hashHandle, derivedHandle);
}

int main(void)
{
    encode_record();
    return 0;
}