#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void run_task()
{
    HCRYPTPROV ctx = 0;
    HCRYPTKEY key = 0;
    HCRYPTHASH hash = 0;

    char secret[100];
    char data[100];
    DWORD dataLen = sizeof(data) - 1;
    size_t n;

    FILE *f = NULL;

    printf("Password: ");
    if (fgets(secret, sizeof(secret), stdin) == NULL)
    {
        secret[0] = '\0';
    }

    n = strlen(secret);
    if (n > 0)
    {
        secret[n - 1] = '\0';
    }

    f = fopen("encrypted.txt", "rb");
    if (!f)
    {
        exit(1);
    }

    if (fread(data, 1, sizeof(data), f) != sizeof(data))
    {
        fclose(f);
        exit(1);
    }

    data[sizeof(data) - 1] = '\0';

    if (!CryptAcquireContext(&ctx, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&ctx, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            exit(1);
        }
    }

    if (!CryptCreateHash(ctx, CALG_SHA_256, 0, 0, &hash))
    {
        exit(1);
    }

    if (!CryptHashData(hash, (BYTE *)secret, (DWORD)n, 0))
    {
        exit(1);
    }

    if (!CryptDeriveKey(ctx, CALG_DES, hash, 0, &key))
    {
        exit(1);
    }

    if (!CryptDecrypt(key, 0, 1, 0, (BYTE *)data, &dataLen))
    {
        exit(1);
    }

    data[dataLen] = '\0';
    printf("%s\n", data);

    if (key)
        CryptDestroyKey(key);
    if (hash)
        CryptDestroyHash(hash);
    if (ctx)
        CryptReleaseContext(ctx, 0);
    if (f)
        fclose(f);
}

int main(void)
{
    run_task();
    return 0;
}