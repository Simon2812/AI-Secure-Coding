#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void process_input()
{
    HCRYPTPROV provider = 0;
    HCRYPTKEY sessionKey = 0;
    HCRYPTHASH digest = 0;

    char input[100];
    char buffer[100];
    DWORD bufferLen = sizeof(buffer) - 1;
    size_t len;

    FILE *fp = NULL;

    printf("Password: ");
    if (fgets(input, sizeof(input), stdin) == NULL)
    {
        input[0] = '\0';
    }

    len = strlen(input);
    if (len > 0)
    {
        input[len - 1] = '\0';
    }

    fp = fopen("encrypted.txt", "rb");
    if (!fp)
    {
        exit(1);
    }

    if (fread(buffer, 1, sizeof(buffer), fp) != sizeof(buffer))
    {
        fclose(fp);
        exit(1);
    }

    buffer[sizeof(buffer) - 1] = '\0';

    if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &digest))
    {
        exit(1);
    }

    if (!CryptHashData(digest, (BYTE *)input, (DWORD)len, 0))
    {
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_3DES, digest, 0, &sessionKey))
    {
        exit(1);
    }

    if (!CryptDecrypt(sessionKey, 0, 1, 0, (BYTE *)buffer, &bufferLen))
    {
        exit(1);
    }

    buffer[bufferLen] = '\0';
    printf("%s\n", buffer);

    if (sessionKey)
        CryptDestroyKey(sessionKey);
    if (digest)
        CryptDestroyHash(digest);
    if (provider)
        CryptReleaseContext(provider, 0);
    if (fp)
        fclose(fp);
}

int main(void)
{
    process_input();
    return 0;
}