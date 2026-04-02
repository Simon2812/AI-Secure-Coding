#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

static void release_crypto(HCRYPTPROV provider, HCRYPTHASH hashHandle, HCRYPTKEY keyHandle)
{
    if (keyHandle)
    {
        CryptDestroyKey(keyHandle);
    }

    if (hashHandle)
    {
        CryptDestroyHash(hashHandle);
    }

    if (provider)
    {
        CryptReleaseContext(provider, 0);
    }
}

void encrypt_data(void)
{
    char keyInput[100] = "";
    HCRYPTPROV provider = 0;
    HCRYPTKEY keyHandle = 0;
    HCRYPTHASH hashHandle = 0;
    char text[] = "String to be encrypted";
    DWORD encryptedLen = (DWORD)strlen(text);
    BYTE encrypted[200];
    FILE *fp = NULL;

    fp = fopen("key.txt", "r");
    if (fp != NULL)
    {
        if (fgets(keyInput, sizeof(keyInput), fp) == NULL)
        {
            keyInput[0] = '\0';
        }
        fclose(fp);

        {
            size_t len = strlen(keyInput);
            if (len > 0 && keyInput[len - 1] == '\n')
            {
                keyInput[len - 1] = '\0';
            }
        }
    }

    memcpy(encrypted, text, encryptedLen);

    if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("Error in acquiring cryptographic context");
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hashHandle))
    {
        puts("Error in creating hash");
        release_crypto(provider, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptHashData(hashHandle, (BYTE *)keyInput, (DWORD)strlen(keyInput), 0))
    {
        puts("Error in hashing key input");
        release_crypto(provider, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, hashHandle, 0, &keyHandle))
    {
        puts("Error in CryptDeriveKey");
        release_crypto(provider, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptEncrypt(keyHandle, (HCRYPTHASH)NULL, 1, 0, encrypted, &encryptedLen, sizeof(encrypted)))
    {
        puts("Error in CryptEncrypt");
        release_crypto(provider, hashHandle, keyHandle);
        exit(1);
    }

    for (DWORD i = 0; i < encryptedLen; i++)
    {
        printf("%02X", encrypted[i]);
    }
    printf("\n");

    release_crypto(provider, hashHandle, keyHandle);
}

int main(void)
{
    encrypt_data();
    return 0;
}