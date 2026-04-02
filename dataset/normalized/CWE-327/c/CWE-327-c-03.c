#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void execute()
{
    HCRYPTPROV prov = 0;
    HCRYPTKEY keyHandle = 0;
    HCRYPTHASH hashHandle = 0;

    char pass[100];
    char content[100];
    DWORD contentLen = sizeof(content) - 1;
    size_t passLen;

    FILE *file = NULL;

    printf("Password: ");
    if (fgets(pass, sizeof(pass), stdin) == NULL)
    {
        pass[0] = '\0';
    }

    passLen = strlen(pass);
    if (passLen > 0)
    {
        pass[passLen - 1] = '\0';
    }

    file = fopen("encrypted.txt", "rb");
    if (!file)
    {
        exit(1);
    }

    if (fread(content, 1, sizeof(content), file) != sizeof(content))
    {
        fclose(file);
        exit(1);
    }

    content[sizeof(content) - 1] = '\0';

    if (!CryptAcquireContext(&prov, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&prov, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            exit(1);
        }
    }

    if (!CryptCreateHash(prov, CALG_SHA_256, 0, 0, &hashHandle))
    {
        exit(1);
    }

    if (!CryptHashData(hashHandle, (BYTE *)pass, (DWORD)passLen, 0))
    {
        exit(1);
    }

    if (!CryptDeriveKey(prov, CALG_RC5, hashHandle, 0, &keyHandle))
    {
        exit(1);
    }

    if (!CryptDecrypt(keyHandle, 0, 1, 0, (BYTE *)content, &contentLen))
    {
        exit(1);
    }

    content[contentLen] = '\0';
    printf("%s\n", content);

    if (keyHandle)
        CryptDestroyKey(keyHandle);
    if (hashHandle)
        CryptDestroyHash(hashHandle);
    if (prov)
        CryptReleaseContext(prov, 0);
    if (file)
        fclose(file);
}

int main(void)
{
    execute();
    return 0;
}