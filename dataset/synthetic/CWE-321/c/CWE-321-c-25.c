#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

static int read_from_file(char *buf, size_t size)
{
    FILE *fp = fopen("primary.cfg", "r");
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

static int read_from_backup(char *buf, size_t size)
{
    FILE *fp = fopen("backup.cfg", "r");
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

static void release_all(HCRYPTPROV ctx, HCRYPTHASH h, HCRYPTKEY k)
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

void process_payload(void)
{
    char material[100] = "";
    int sourceSelector = 1;

    switch (sourceSelector)
    {
        case 0:
            if (!read_from_file(material, sizeof(material)))
            {
                material[0] = '\0';
            }
            break;
        case 1:
            if (!read_from_backup(material, sizeof(material)))
            {
                material[0] = '\0';
            }
            break;
        default:
        {
            char *env = getenv("FALLBACK_SECRET");
            if (env != NULL)
            {
                strncpy(material, env, sizeof(material) - 1);
                material[sizeof(material) - 1] = '\0';
            }
        }
            break;
    }

    HCRYPTPROV ctx = 0;
    HCRYPTKEY keyObj = 0;
    HCRYPTHASH hashObj = 0;

    char payload[] = "archive block";
    DWORD len = (DWORD)strlen(payload);
    BYTE out[200];

    memcpy(out, payload, len);

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

    if (!CryptEncrypt(keyObj, 0, 1, 0, out, &len, sizeof(out)))
    {
        puts("encrypt error");
        release_all(ctx, hashObj, keyObj);
        exit(1);
    }

    for (DWORD i = 0; i < len; i++)
    {
        printf("%02X", out[i]);
    }
    printf("\n");

    release_all(ctx, hashObj, keyObj);
}

int main(void)
{
    process_payload();
    return 0;
}
