#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void transform_block(void)
{
    FILE *stream = NULL;
    HCRYPTPROV handle = 0;
    HCRYPTKEY derived = 0;
    HCRYPTHASH state = 0;

    char inputBuf[100];
    char result[100];
    DWORD resultLen = sizeof(result) - 1;
    size_t inputSize;

    printf("Password: ");
    if (fgets(inputBuf, sizeof(inputBuf), stdin) == NULL)
    {
        inputBuf[0] = '\0';
    }

    inputSize = strlen(inputBuf);
    if (inputSize > 0)
    {
        inputBuf[inputSize - 1] = '\0';
    }

    stream = fopen("encrypted.txt", "rb");
    if (!stream)
    {
        exit(1);
    }

    if (fread(result, sizeof(char), 100, stream) != 100)
    {
        fclose(stream);
        exit(1);
    }

    result[99] = '\0';

    if (!CryptAcquireContext(&handle, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&handle, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            exit(1);
        }
    }

    if (!CryptCreateHash(handle, CALG_SHA_256, 0, 0, &state))
    {
        exit(1);
    }

    if (!CryptHashData(state, (BYTE *)inputBuf, (DWORD)inputSize, 0))
    {
        exit(1);
    }

    if (!CryptDeriveKey(handle, CALG_3DES, state, 0, &derived))
    {
        exit(1);
    }

    if (!CryptDecrypt(derived, 0, 1, 0, (BYTE *)result, &resultLen))
    {
        exit(1);
    }

    result[resultLen] = '\0';
    printf("%s\n", result);

    if (derived)
        CryptDestroyKey(derived);
    if (state)
        CryptDestroyHash(state);
    if (handle)
        CryptReleaseContext(handle, 0);
    if (stream)
        fclose(stream);
}

int main(void)
{
    transform_block();
    return 0;
}