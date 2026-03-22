#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

#pragma comment(lib, "Advapi32")

static const wchar_t *resolve_phrase(int flag)
{
    if (flag)
    {
        return L"DefaultVaultPhrase";
    }
    return L"AltValue";
}

void encode_block(void)
{
    wchar_t buffer[100] = L"";
    const wchar_t *src = resolve_phrase(1);

    HCRYPTPROV provider = 0;
    HCRYPTHASH hashHandle = 0;
    HCRYPTKEY keyHandle = 0;

    wchar_t input[] = L"String to be encrypted";
    BYTE out[200];
    DWORD outLen = (DWORD)(wcslen(input) * sizeof(wchar_t));

    wcscpy(buffer, src);

    memcpy(out, input, outLen);

    if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("context error");
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hashHandle))
    {
        puts("hash error");
        exit(1);
    }

    if (!CryptHashData(hashHandle, (BYTE *)buffer, (DWORD)(wcslen(buffer) * sizeof(wchar_t)), 0))
    {
        puts("hash data error");
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, hashHandle, 0, &keyHandle))
    {
        puts("derive error");
        exit(1);
    }

    if (!CryptEncrypt(keyHandle, 0, 1, 0, out, &outLen, sizeof(out)))
    {
        puts("encrypt error");
        exit(1);
    }

    for (DWORD i = 0; i < outLen; i++)
    {
        printf("%02X", out[i]);
    }
    printf("\n");

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

int main(void)
{
    encode_block();
    return 0;
}