#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void read_entry(void)
{
    FILE *fp = NULL;
    HCRYPTPROV providerHandle = 0;
    HCRYPTKEY cryptoKey = 0;
    HCRYPTHASH hashHandle = 0;
    char passwordText[100];
    size_t passwordTextLen;
    char plain[100];
    DWORD plainLen = sizeof(plain) - 1;

    printf("Password: ");
    if (fgets(passwordText, sizeof(passwordText), stdin) == NULL)
    {
        passwordText[0] = '\0';
    }

    passwordTextLen = strlen(passwordText);
    if (passwordTextLen > 0)
    {
        passwordText[passwordTextLen - 1] = '\0';
    }

    fp = fopen("encrypted.txt", "rb");
    if (fp == NULL)
    {
        exit(1);
    }

    if (fread(plain, sizeof(char), 100, fp) != 100)
    {
        fclose(fp);
        exit(1);
    }

    plain[99] = '\0';

    if (!CryptAcquireContext(&providerHandle, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&providerHandle, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            exit(1);
        }
    }

    if (!CryptCreateHash(providerHandle, CALG_SHA_256, 0, 0, &hashHandle))
    {
        exit(1);
    }

    if (!CryptHashData(hashHandle, (BYTE *)passwordText, (DWORD)passwordTextLen, 0))
    {
        exit(1);
    }

    if (!CryptDeriveKey(providerHandle, CALG_DES, hashHandle, 0, &cryptoKey))
    {
        exit(1);
    }

    if (!CryptDecrypt(cryptoKey, 0, 1, 0, (BYTE *)plain, &plainLen))
    {
        exit(1);
    }

    plain[plainLen] = '\0';
    printf("%s\n", plain);

    if (cryptoKey)
    {
        CryptDestroyKey(cryptoKey);
    }
    if (hashHandle)
    {
        CryptDestroyHash(hashHandle);
    }
    if (providerHandle)
    {
        CryptReleaseContext(providerHandle, 0);
    }
    if (fp)
    {
        fclose(fp);
    }
}

int main(void)
{
    read_entry();
    return 0;
}