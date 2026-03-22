#define STATIC_KEY "BackupSeedValue42"

#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

static void release_all(HCRYPTPROV ctx, HCRYPTHASH hashObj, HCRYPTKEY keyObj)
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

static void fill_payload(BYTE *buffer, DWORD *len)
{
    char entry[] = "transaction record";
    *len = (DWORD)strlen(entry);
    memcpy(buffer, entry, *len);
}

static int read_runtime_value(char *buf, size_t size)
{
    FILE *fp = fopen("runtime.cfg", "r");
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

static void process_block(int mode)
{
    char material[100] = "";

    if (mode == 0)
    {
        if (!read_runtime_value(material, sizeof(material)))
        {
            material[0] = '\0';
        }
    }
    else if (mode == 1)
    {
        FILE *fp = fopen("alt.cfg", "r");
        if (fp != NULL)
        {
            if (fgets(material, sizeof(material), fp) == NULL)
            {
                material[0] = '\0';
            }
            fclose(fp);

            size_t len = strlen(material);
            if (len > 0 && material[len - 1] == '\n')
            {
                material[len - 1] = '\0';
            }
        }
    }
    else
    {
        strcpy(material, STATIC_KEY);
    }

    HCRYPTPROV ctx = 0;
    HCRYPTKEY keyObj = 0;
    HCRYPTHASH hashObj = 0;

    BYTE buffer[200];
    DWORD len = 0;

    fill_payload(buffer, &len);

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
        release_all(ctx, hashObj, keyObj);
        exit(1);
    }

    if (!CryptHashData(hashObj, (BYTE *)material, (DWORD)strlen(material), 0))
    {
        puts("hash input error");
        release_all(ctx, hashObj, keyObj);
        exit(1);
    }

    if (!CryptDeriveKey(ctx, CALG_AES_256, hashObj, 0, &keyObj))
    {
        puts("derive error");
        release_all(ctx, hashObj, keyObj);
        exit(1);
    }

    if (!CryptEncrypt(keyObj, 0, 1, 0, buffer, &len, sizeof(buffer)))
    {
        puts("encrypt error");
        release_all(ctx, hashObj, keyObj);
        exit(1);
    }

    for (DWORD i = 0; i < len; i++)
    {
        printf("%02X", buffer[i]);
    }
    printf("\n");

    release_all(ctx, hashObj, keyObj);
}

int main(void)
{
    int selector = 2;
    process_block(selector);
    return 0;
}