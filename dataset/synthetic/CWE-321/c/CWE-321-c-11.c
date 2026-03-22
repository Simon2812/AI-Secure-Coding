#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

static void fill_buffer(char *dst, size_t cap)
{
    const char *value = "LocalSeed";
    strncpy(dst, value, cap - 1);
    dst[cap - 1] = '\0';
}

void transform(void)
{
    char dataBuf[100] = "";
    HCRYPTPROV ctx = 0;
    HCRYPTHASH hash = 0;
    HCRYPTKEY key = 0;
    char input[] = "String to be encrypted";
    BYTE out[200];
    DWORD outLen = (DWORD)strlen(input);

    fill_buffer(dataBuf, sizeof(dataBuf));

    memcpy(out, input, outLen);

    if (!CryptAcquireContext(&ctx, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&ctx, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("context error");
            exit(1);
        }
    }

    if (!CryptCreateHash(ctx, CALG_SHA_256, 0, 0, &hash))
    {
        puts("hash error");
        exit(1);
    }

    if (!CryptHashData(hash, (BYTE *)dataBuf, (DWORD)strlen(dataBuf), 0))
    {
        puts("hash data error");
        exit(1);
    }

    if (!CryptDeriveKey(ctx, CALG_AES_256, hash, 0, &key))
    {
        puts("derive error");
        exit(1);
    }

    if (!CryptEncrypt(key, 0, 1, 0, out, &outLen, sizeof(out)))
    {
        puts("encrypt error");
        exit(1);
    }

    for (DWORD i = 0; i < outLen; i++)
    {
        printf("%02X", out[i]);
    }
    printf("\n");

    if (key) CryptDestroyKey(key);
    if (hash) CryptDestroyHash(hash);
    if (ctx) CryptReleaseContext(ctx, 0);
}

int main(void)
{
    transform();
    return 0;
}