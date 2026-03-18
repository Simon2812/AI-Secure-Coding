#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void show_entry(void)
{
    FILE *file = NULL;
    HCRYPTPROV provider = 0;
    HCRYPTHASH hash = 0;
    HCRYPTKEY key = 0;

    char secret[100];
    char text[100];
    DWORD textLen = sizeof(text) - 1;
    size_t secretLen;

    printf("Enter password: ");
    if (fgets(secret, sizeof(secret), stdin) == NULL)
    {
        secret[0] = '\0';
    }

    secretLen = strlen(secret);
    if (secretLen > 0)
    {
        secret[secretLen - 1] = '\0';
    }

    file = fopen("encrypted.txt", "rb");
    if (file == NULL)
    {
        exit(1);
    }

    if (fread(text, sizeof(char), 100, file) != 100)
    {
        fclose(file);
        exit(1);
    }

    text[99] = '\0';

    if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            fclose(file);
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hash))
    {
        CryptReleaseContext(provider, 0);
        fclose(file);
        exit(1);
    }

    if (!CryptHashData(hash, (BYTE *)secret, (DWORD)secretLen, 0))
    {
        CryptDestroyHash(hash);
        CryptReleaseContext(provider, 0);
        fclose(file);
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, hash, 0, &key))
    {
        CryptDestroyHash(hash);
        CryptReleaseContext(provider, 0);
        fclose(file);
        exit(1);
    }

    if (!CryptDecrypt(key, 0, TRUE, 0, (BYTE *)text, &textLen))
    {
        CryptDestroyKey(key);
        CryptDestroyHash(hash);
        CryptReleaseContext(provider, 0);
        fclose(file);
        exit(1);
    }

    text[textLen] = '\0';
    puts(text);

    CryptDestroyKey(key);
    CryptDestroyHash(hash);
    CryptReleaseContext(provider, 0);
    fclose(file);
}

int main(void)
{
    show_entry();
    return 0;
}