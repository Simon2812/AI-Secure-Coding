#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

static int load_config_value(char *buf, size_t size)
{
    FILE *fp = fopen("app.cfg", "r");
    if (fp == NULL)
    {
        return 0;
    }

    if (fgets(buf, (int)size, fp) == NULL)
    {
        buf[0] = '\0';
        fclose(fp);
        return 0;
    }

    fclose(fp);

    size_t len = strlen(buf);
    if (len > 0 && buf[len - 1] == '\n')
    {
        buf[len - 1] = '\0';
    }

    return 1;
}

static void release_ctx(HCRYPTPROV ctx, HCRYPTHASH h, HCRYPTKEY k)
{
    if (k)
    {
        CryptDestroyKey(k);
    }
    if (h)
    {
        CryptDestroyHash(h);
    }
    if (ctx)
    {
        CryptReleaseContext(ctx, 0);
    }
}

void store_report(void)
{
    char configValue[100] = "";

    load_config_value(configValue, sizeof(configValue));

    HCRYPTPROV ctx = 0;
    HCRYPTKEY keyObj = 0;
    HCRYPTHASH hashObj = 0;

    char report[] = "audit log";
    DWORD reportLen = (DWORD)strlen(report);
    BYTE output[200];

    memcpy(output, report, reportLen);

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
        release_ctx(ctx, hashObj, keyObj);
        exit(1);
    }

    if (!CryptHashData(hashObj, (BYTE *)configValue, (DWORD)strlen(configValue), 0))
    {
        puts("hash input error");
        release_ctx(ctx, hashObj, keyObj);
        exit(1);
    }

    if (!CryptDeriveKey(ctx, CALG_AES_256, hashObj, 0, &keyObj))
    {
        puts("derive error");
        release_ctx(ctx, hashObj, keyObj);
        exit(1);
    }

    if (!CryptEncrypt(keyObj, 0, 1, 0, output, &reportLen, sizeof(output)))
    {
        puts("encrypt error");
        release_ctx(ctx, hashObj, keyObj);
        exit(1);
    }

    for (DWORD i = 0; i < reportLen; i++)
    {
        printf("%02X", output[i]);
    }
    printf("\n");

    release_ctx(ctx, hashObj, keyObj);
}

int main(void)
{
    store_report();
    return 0;
}