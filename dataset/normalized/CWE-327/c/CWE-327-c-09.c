#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void show_value(void)
{
    FILE *dataFile = NULL;
    HCRYPTPROV cryptoProvider = 0;
    HCRYPTKEY workingKey = 0;
    HCRYPTHASH hashValue = 0;
    char entry[100];
    size_t entryLen;
    char buffer[100];
    DWORD bufferLen = sizeof(buffer) - 1;

    printf("Password: ");
    if (fgets(entry, sizeof(entry), stdin) == NULL)
    {
        entry[0] = '\0';
    }

    entryLen = strlen(entry);
    if (entryLen > 0)
    {
        entry[entryLen - 1] = '\0';
    }

    dataFile = fopen("encrypted.txt", "rb");
    if (dataFile == NULL)
    {
        exit(1);
    }

    if (fread(buffer, sizeof(char), 100, dataFile) != 100)
    {
        fclose(dataFile);
        exit(1);
    }

    buffer[99] = '\0';

    if (!CryptAcquireContext(&cryptoProvider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&cryptoProvider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            exit(1);
        }
    }

    if (!CryptCreateHash(cryptoProvider, CALG_SHA_256, 0, 0, &hashValue))
    {
        exit(1);
    }

    if (!CryptHashData(hashValue, (BYTE *)entry, (DWORD)entryLen, 0))
    {
        exit(1);
    }

    if (!CryptDeriveKey(cryptoProvider, CALG_RC5, hashValue, 0, &workingKey))
    {
        exit(1);
    }

    if (!CryptDecrypt(workingKey, 0, 1, 0, (BYTE *)buffer, &bufferLen))
    {
        exit(1);
    }

    buffer[bufferLen] = '\0';
    printf("%s\n", buffer);

    if (workingKey)
    {
        CryptDestroyKey(workingKey);
    }
    if (hashValue)
    {
        CryptDestroyHash(hashValue);
    }
    if (cryptoProvider)
    {
        CryptReleaseContext(cryptoProvider, 0);
    }
    if (dataFile)
    {
        fclose(dataFile);
    }
}

int main(void)
{
    show_value();
    return 0;
}