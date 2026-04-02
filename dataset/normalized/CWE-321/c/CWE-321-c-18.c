#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

#pragma comment(lib, "Advapi32")

static void release_crypto(HCRYPTPROV provider, HCRYPTHASH hashHandle, HCRYPTKEY keyHandle)
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

void encrypt_record(void)
{
    wchar_t keyInput[100] = L"";
    HCRYPTPROV provider = 0;
    HCRYPTKEY keyHandle = 0;
    HCRYPTHASH hashHandle = 0;
    wchar_t payload[] = L"Quarterly report";
    DWORD dataLen = (DWORD)(wcslen(payload) * sizeof(wchar_t));
    BYTE cipherText[200];

    GetPrivateProfileStringW(L"crypto", L"key", L"", keyInput, 100, L".\\app.ini");

    memcpy(cipherText, payload, dataLen);

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
        release_crypto(provider, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptHashData(hashHandle, (BYTE *)keyInput, (DWORD)(wcslen(keyInput) * sizeof(wchar_t)), 0))
    {
        puts("Error in hashing key input");
        release_crypto(provider, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, hashHandle, 0, &keyHandle))
    {
        puts("Error in CryptDeriveKey");
        release_crypto(provider, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptEncrypt(keyHandle, (HCRYPTHASH)NULL, 1, 0, cipherText, &dataLen, sizeof(cipherText)))
    {
        puts("Error in CryptEncrypt");
        release_crypto(provider, hashHandle, keyHandle);
        exit(1);
    }

    for (DWORD i = 0; i < dataLen; i++)
    {
        printf("%02X", cipherText[i]);
    }
    printf("\n");

    release_crypto(provider, hashHandle, keyHandle);
}

int main(void)
{
    encrypt_record();
    return 0;
}