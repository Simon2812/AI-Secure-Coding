#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void decode_file(void)
{
    FILE *handle = NULL;
    HCRYPTPROV context = 0;
    HCRYPTKEY keyObj = 0;
    HCRYPTHASH hashObj = 0;

    char userInput[100];
    char output[100];
    DWORD outputLen = sizeof(output) - 1;
    size_t inputLen;

    printf("Password: ");
    if (fgets(userInput, sizeof(userInput), stdin) == NULL)
    {
        userInput[0] = '\0';
    }

    inputLen = strlen(userInput);
    if (inputLen > 0)
    {
        userInput[inputLen - 1] = '\0';
    }

    handle = fopen("encrypted.txt", "rb");
    if (!handle)
    {
        exit(1);
    }

    if (fread(output, sizeof(char), 100, handle) != 100)
    {
        fclose(handle);
        exit(1);
    }

    output[99] = '\0';

    if (!CryptAcquireContext(&context, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&context, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            exit(1);
        }
    }

    if (!CryptCreateHash(context, CALG_SHA_256, 0, 0, &hashObj))
    {
        exit(1);
    }

    if (!CryptHashData(hashObj, (BYTE *)userInput, (DWORD)inputLen, 0))
    {
        exit(1);
    }

    if (!CryptDeriveKey(context, CALG_DES, hashObj, 0, &keyObj))
    {
        exit(1);
    }

    if (!CryptDecrypt(keyObj, 0, 1, 0, (BYTE *)output, &outputLen))
    {
        exit(1);
    }

    output[outputLen] = '\0';
    printf("%s\n", output);

    if (keyObj)
        CryptDestroyKey(keyObj);
    if (hashObj)
        CryptDestroyHash(hashObj);
    if (context)
        CryptReleaseContext(context, 0);
    if (handle)
        fclose(handle);
}

int main(void)
{
    decode_file();
    return 0;
}