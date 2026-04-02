#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static HCRYPTPROV open_provider(void)
{
    HCRYPTPROV provider = 0;

    if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            return 0;
        }
    }

    return provider;
}

static HCRYPTHASH hash_phrase(HCRYPTPROV provider, const char *phrase)
{
    HCRYPTHASH hashObj = 0;

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hashObj))
    {
        return 0;
    }

    if (!CryptHashData(hashObj, (BYTE *)phrase, (DWORD)strlen(phrase), 0))
    {
        CryptDestroyHash(hashObj);
        return 0;
    }

    return hashObj;
}

static HCRYPTKEY make_first_key(HCRYPTPROV provider, HCRYPTHASH hashObj)
{
    HCRYPTKEY keyObj = 0;

    if (!CryptDeriveKey(provider, CALG_DES, hashObj, 0, &keyObj))
    {
        return 0;
    }

    return keyObj;
}

static HCRYPTKEY make_second_key(HCRYPTPROV provider, HCRYPTHASH hashObj)
{
    HCRYPTKEY keyObj = 0;

    if (!CryptDeriveKey(provider, CALG_RC4, hashObj, 0, &keyObj))
    {
        return 0;
    }

    return keyObj;
}

int main(void)
{
    FILE *inputFile = NULL;
    HCRYPTPROV provider = 0;
    HCRYPTHASH hashObj = 0;
    HCRYPTKEY fileKey = 0;
    HCRYPTKEY lineKey = 0;

    char phrase[80];
    char block[128];
    DWORD blockLen = sizeof(block) - 1;

    inputFile = fopen("encrypted.txt", "rb");
    if (inputFile == NULL)
    {
        return 1;
    }

    if (fread(block, 1, sizeof(block), inputFile) == 0)
    {
        fclose(inputFile);
        return 1;
    }
    fclose(inputFile);

    printf("Password: ");
    if (fgets(phrase, sizeof(phrase), stdin) == NULL)
    {
        return 1;
    }

    phrase[strcspn(phrase, "\n")] = '\0';

    provider = open_provider();
    if (!provider)
    {
        return 1;
    }

    hashObj = hash_phrase(provider, phrase);
    if (!hashObj)
    {
        CryptReleaseContext(provider, 0);
        return 1;
    }

    fileKey = make_first_key(provider, hashObj);
    lineKey = make_second_key(provider, hashObj);
    if (!fileKey || !lineKey)
    {
        if (fileKey)
        {
            CryptDestroyKey(fileKey);
        }
        if (lineKey)
        {
            CryptDestroyKey(lineKey);
        }
        CryptDestroyHash(hashObj);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptDecrypt(fileKey, 0, TRUE, 0, (BYTE *)block, &blockLen))
    {
        CryptDestroyKey(fileKey);
        CryptDestroyKey(lineKey);
        CryptDestroyHash(hashObj);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    block[blockLen] = '\0';
    puts(block);

    CryptDestroyKey(fileKey);
    CryptDestroyKey(lineKey);
    CryptDestroyHash(hashObj);
    CryptReleaseContext(provider, 0);

    return 0;
}