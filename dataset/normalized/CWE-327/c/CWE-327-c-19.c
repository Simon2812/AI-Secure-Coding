#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void open_text(void)
{
    FILE *source = NULL;
    HCRYPTPROV provider = 0;
    HCRYPTHASH digest = 0;
    HCRYPTKEY key = 0;

    char password[100];
    char data[100];
    DWORD dataLen = sizeof(data) - 1;
    size_t passwordLen;

    printf("Enter password: ");
    if (fgets(password, sizeof(password), stdin) == NULL)
    {
        password[0] = '\0';
    }

    passwordLen = strlen(password);
    if (passwordLen > 0)
    {
        password[passwordLen - 1] = '\0';
    }

    source = fopen("encrypted.txt", "rb");
    if (source == NULL)
    {
        exit(1);
    }

    if (fread(data, sizeof(char), 100, source) != 100)
    {
        fclose(source);
        exit(1);
    }

    data[99] = '\0';

    if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            fclose(source);
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &digest))
    {
        CryptReleaseContext(provider, 0);
        fclose(source);
        exit(1);
    }

    if (!CryptHashData(digest, (BYTE *)password, (DWORD)passwordLen, 0))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(provider, 0);
        fclose(source);
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, digest, 0, &key))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(provider, 0);
        fclose(source);
        exit(1);
    }

    if (!CryptDecrypt(key, 0, TRUE, 0, (BYTE *)data, &dataLen))
    {
        CryptDestroyKey(key);
        CryptDestroyHash(digest);
        CryptReleaseContext(provider, 0);
        fclose(source);
        exit(1);
    }

    data[dataLen] = '\0';
    puts(data);

    CryptDestroyKey(key);
    CryptDestroyHash(digest);
    CryptReleaseContext(provider, 0);
    fclose(source);
}

int main(void)
{
    open_text();
    return 0;
}