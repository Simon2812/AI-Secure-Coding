#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

static const int useFileSource = 1;
static const int useFallback = 0;

static void cleanup(HCRYPTPROV provider, HCRYPTHASH hashHandle, HCRYPTKEY keyHandle)
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

void protect_text(void)
{
    char inputBuffer[100] = "";
    HCRYPTPROV provider = 0;
    HCRYPTKEY keyHandle = 0;
    HCRYPTHASH hashHandle = 0;
    char plainText[] = "String to be encrypted";
    DWORD dataLen = (DWORD)strlen(plainText);
    BYTE cipherText[200];

    if (useFileSource)
    {
        FILE *fp = fopen("key.txt", "r");
        if (fp != NULL)
        {
            if (fgets(inputBuffer, sizeof(inputBuffer), fp) == NULL)
            {
                inputBuffer[0] = '\0';
            }
            fclose(fp);

            {
                size_t len = strlen(inputBuffer);
                if (len > 0 && inputBuffer[len - 1] == '\n')
                {
                    inputBuffer[len - 1] = '\0';
                }
            }
        }
    }

    if (useFallback)
    {
        strcpy(inputBuffer, "unused");
    }

    memcpy(cipherText, plainText, dataLen);

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
        cleanup(provider, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptHashData(hashHandle, (BYTE *)inputBuffer, (DWORD)strlen(inputBuffer), 0))
    {
        puts("Error in hashing input");
        cleanup(provider, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, hashHandle, 0, &keyHandle))
    {
        puts("Error in CryptDeriveKey");
        cleanup(provider, hashHandle, keyHandle);
        exit(1);
    }

    if (!CryptEncrypt(keyHandle, (HCRYPTHASH)NULL, 1, 0, cipherText, &dataLen, sizeof(cipherText)))
    {
        puts("Error in CryptEncrypt");
        cleanup(provider, hashHandle, keyHandle);
        exit(1);
    }

    for (DWORD i = 0; i < dataLen; i++)
    {
        printf("%02X", cipherText[i]);
    }
    printf("\n");

    cleanup(provider, hashHandle, keyHandle);
}

int main(void)
{
    protect_text();
    return 0;
}