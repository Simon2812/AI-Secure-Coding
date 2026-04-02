#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void run()
{
    FILE *f;
    HCRYPTPROV prov = 0;
    HCRYPTHASH hash = 0;
    HCRYPTKEY key = 0;

    char input[100];
    char data[100];
    DWORD dataLen = sizeof(data) - 1;
    size_t len;

    printf("Enter password: ");
    if (fgets(input, sizeof(input), stdin) == NULL)
    {
        input[0] = '\0';
    }

    len = strlen(input);
    if (len > 0)
    {
        input[len - 1] = '\0';
    }

    f = fopen("encrypted.txt", "rb");
    if (!f)
    {
        exit(1);
    }

    if (fread(data, sizeof(char), 100, f) != 100)
    {
        fclose(f);
        exit(1);
    }

    data[99] = '\0';

    if (!CryptAcquireContext(&prov, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&prov, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            fclose(f);
            exit(1);
        }
    }

    if (!CryptCreateHash(prov, CALG_SHA_256, 0, 0, &hash))
    {
        CryptReleaseContext(prov, 0);
        fclose(f);
        exit(1);
    }

    if (!CryptHashData(hash, (BYTE *)input, (DWORD)len, 0))
    {
        CryptDestroyHash(hash);
        CryptReleaseContext(prov, 0);
        fclose(f);
        exit(1);
    }

    if (!CryptDeriveKey(prov, CALG_AES_256, hash, 0, &key))
    {
        CryptDestroyHash(hash);
        CryptReleaseContext(prov, 0);
        fclose(f);
        exit(1);
    }

    if (!CryptDecrypt(key, 0, TRUE, 0, (BYTE *)data, &dataLen))
    {
        CryptDestroyKey(key);
        CryptDestroyHash(hash);
        CryptReleaseContext(prov, 0);
        fclose(f);
        exit(1);
    }

    data[dataLen] = '\0';
    puts(data);

    CryptDestroyKey(key);
    CryptDestroyHash(hash);
    CryptReleaseContext(prov, 0);
    fclose(f);
}

int main(void)
{
    run();
    return 0;
}