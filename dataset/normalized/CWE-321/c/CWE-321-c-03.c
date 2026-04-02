#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

#define BOOTSTRAP_SECRET "LocalStageSeed"

static int enabled = 1;
static int disabled = 0;

static void release_resources(HCRYPTPROV provider, HCRYPTHASH digest, HCRYPTKEY aesKey)
{
    if (aesKey)
    {
        CryptDestroyKey(aesKey);
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

void protect_buffer(void)
{
    char keySource[100] = "";
    HCRYPTPROV provider = 0;
    HCRYPTHASH digest = 0;
    HCRYPTKEY aesKey = 0;
    char text[] = "String to be encrypted";
    BYTE block[200];
    DWORD blockLen = (DWORD)strlen(text);

    if (enabled)
    {
        strcpy(keySource, BOOTSTRAP_SECRET);
    }

    memcpy(block, text, blockLen);

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
        release_resources(provider, digest, aesKey);
        exit(1);
    }

    if (!CryptHashData(digest, (BYTE *)keySource, (DWORD)strlen(keySource), 0))
    {
        puts("hash data error");
        release_resources(provider, digest, aesKey);
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, digest, 0, &aesKey))
    {
        puts("derive error");
        release_resources(provider, digest, aesKey);
        exit(1);
    }

    if (!CryptEncrypt(aesKey, 0, 1, 0, block, &blockLen, sizeof(block)))
    {
        puts("encrypt error");
        release_resources(provider, digest, aesKey);
        exit(1);
    }

    for (DWORD i = 0; i < blockLen; i++)
    {
        printf("%02X", block[i]);
    }
    printf("\n");

    release_resources(provider, digest, aesKey);
}

int main(void)
{
    if (disabled)
    {
        return 0;
    }

    protect_buffer();
    return 0;
}