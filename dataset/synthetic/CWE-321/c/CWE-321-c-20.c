#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

static void cleanup(HCRYPTPROV ctx, HCRYPTHASH digest, HCRYPTKEY key)
{
    if (key)
    {
        CryptDestroyKey(key);
    }
    if (digest)
    {
        CryptDestroyHash(digest);
    }
    if (ctx)
    {
        CryptReleaseContext(ctx, 0);
    }
}

void process_record(void)
{
    char sourceBuf[100] = "";
    FILE *fp = fopen("key.txt", "r");

    if (fp != NULL)
    {
        if (fgets(sourceBuf, sizeof(sourceBuf), fp) == NULL)
        {
            sourceBuf[0] = '\0';
        }
        fclose(fp);

        size_t len = strlen(sourceBuf);
        if (len > 0 && sourceBuf[len - 1] == '\n')
        {
            sourceBuf[len - 1] = '\0';
        }
    }

    HCRYPTPROV ctx = 0;
    HCRYPTKEY derivedKey = 0;
    HCRYPTHASH digest = 0;

    char payload[] = "log entry";
    DWORD dataLen = (DWORD)strlen(payload);
    BYTE buffer[200];

    memcpy(buffer, payload, dataLen);

    if (!CryptAcquireContext(&ctx, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&ctx, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("context error");
            exit(1);
        }
    }

    if (!CryptCreateHash(ctx, CALG_SHA_256, 0, 0, &digest))
    {
        puts("hash error");
        cleanup(ctx, digest, derivedKey);
        exit(1);
    }

    if (!CryptHashData(digest, (BYTE *)sourceBuf, (DWORD)strlen(sourceBuf), 0))
    {
        puts("data error");
        cleanup(ctx, digest, derivedKey);
        exit(1);
    }

    if (!CryptDeriveKey(ctx, CALG_AES_256, digest, 0, &derivedKey))
    {
        puts("derive error");
        cleanup(ctx, digest, derivedKey);
        exit(1);
    }

    if (!CryptEncrypt(derivedKey, 0, 1, 0, buffer, &dataLen, sizeof(buffer)))
    {
        puts("encrypt error");
        cleanup(ctx, digest, derivedKey);
        exit(1);
    }

    for (DWORD i = 0; i < dataLen; i++)
    {
        printf("%02X", buffer[i]);
    }
    printf("\n");

    cleanup(ctx, digest, derivedKey);
}

int main(void)
{
    process_record();
    return 0;
}