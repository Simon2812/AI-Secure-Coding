#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

#define STATIC_TOKEN "Hardcoded"

static void cleanup(HCRYPTPROV ctx, HCRYPTHASH hashObj, HCRYPTKEY keyObj)
{
    if (keyObj)
    {
        CryptDestroyKey(keyObj);
    }

    if (hashObj)
    {
        CryptDestroyHash(hashObj);
    }

    if (ctx)
    {
        CryptReleaseContext(ctx, 0);
    }
}

void process(void)
{
    char material[100] = "";
    HCRYPTPROV ctx = 0;
    HCRYPTHASH hashObj = 0;
    HCRYPTKEY keyObj = 0;
    char input[] = "String to be encrypted";
    BYTE out[200];
    DWORD outLen = (DWORD)strlen(input);

    strcpy(material, STATIC_TOKEN);

    memcpy(out, input, outLen);

    if (!CryptAcquireContext(&ctx, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&ctx, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("context error");
            exit(1);
        }
    }

    if (!CryptCreateHash(ctx, CALG_SHA_256, 0, 0, &hashObj))
    {
        puts("hash error");
        cleanup(ctx, hashObj, keyObj);
        exit(1);
    }

    if (!CryptHashData(hashObj, (BYTE *)material, (DWORD)strlen(material), 0))
    {
        puts("hash data error");
        cleanup(ctx, hashObj, keyObj);
        exit(1);
    }

    if (!CryptDeriveKey(ctx, CALG_AES_256, hashObj, 0, &keyObj))
    {
        puts("derive error");
        cleanup(ctx, hashObj, keyObj);
        exit(1);
    }

    if (!CryptEncrypt(keyObj, 0, 1, 0, out, &outLen, sizeof(out)))
    {
        puts("encrypt error");
        cleanup(ctx, hashObj, keyObj);
        exit(1);
    }

    for (DWORD i = 0; i < outLen; i++)
    {
        printf("%02X", out[i]);
    }
    printf("\n");

    cleanup(ctx, hashObj, keyObj);
}

int main(void)
{
    process();
    return 0;
}