#define STATIC_KEY "DefaultPassphrase123"

#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

static void cleanup_all(HCRYPTPROV ctx, HCRYPTHASH hashObj, HCRYPTKEY keyObj)
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

static void prepare_data(BYTE *buffer, DWORD *len)
{
    char record[] = "internal audit entry";
    *len = (DWORD)strlen(record);
    memcpy(buffer, record, *len);
}

static void derive_and_encrypt(const char *material, BYTE *buffer, DWORD *len)
{
    HCRYPTPROV ctx = 0;
    HCRYPTKEY keyObj = 0;
    HCRYPTHASH hashObj = 0;

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
        cleanup_all(ctx, hashObj, keyObj);
        exit(1);
    }

    if (!CryptHashData(hashObj, (BYTE *)material, (DWORD)strlen(material), 0))
    {
        puts("hash data error");
        cleanup_all(ctx, hashObj, keyObj);
        exit(1);
    }

    if (!CryptDeriveKey(ctx, CALG_AES_256, hashObj, 0, &keyObj))
    {
        puts("derive error");
        cleanup_all(ctx, hashObj, keyObj);
        exit(1);
    }

    if (!CryptEncrypt(keyObj, 0, 1, 0, buffer, len, 200))
    {
        puts("encrypt error");
        cleanup_all(ctx, hashObj, keyObj);
        exit(1);
    }

    cleanup_all(ctx, hashObj, keyObj);
}

static void process_flow(int mode)
{
    char materialBuf[100] = "";

    if (mode == 0)
    {
        FILE *fp = fopen("config.txt", "r");
        if (fp != NULL)
        {
            if (fgets(materialBuf, sizeof(materialBuf), fp) == NULL)
            {
                materialBuf[0] = '\0';
            }
            fclose(fp);
        }
    }
    else if (mode == 1)
    {
        char *env = getenv("ALT_SECRET");
        if (env != NULL)
        {
            strncpy(materialBuf, env, sizeof(materialBuf) - 1);
            materialBuf[sizeof(materialBuf) - 1] = '\0';
        }
    }
    else
    {
        strcpy(materialBuf, STATIC_KEY);
    }

    BYTE buffer[200];
    DWORD len = 0;

    prepare_data(buffer, &len);
    derive_and_encrypt(materialBuf, buffer, &len);

    for (DWORD i = 0; i < len; i++)
    {
        printf("%02X", buffer[i]);
    }
    printf("\n");
}

int main(void)
{
    int selector = 2;
    process_flow(selector);
    return 0;
}