#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void display_record(void)
{
    FILE *input = NULL;
    HCRYPTPROV provider = 0;
    HCRYPTHASH digest = 0;
    HCRYPTKEY key = 0;

    char password[100];
    char content[100];
    DWORD contentLen = sizeof(content) - 1;
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

    input = fopen("encrypted.txt", "rb");
    if (input == NULL)
    {
        exit(1);
    }

    if (fread(content, sizeof(char), 100, input) != 100)
    {
        fclose(input);
        exit(1);
    }

    content[99] = '\0';

    if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            fclose(input);
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &digest))
    {
        CryptReleaseContext(provider, 0);
        fclose(input);
        exit(1);
    }

    if (!CryptHashData(digest, (BYTE *)password, (DWORD)passwordLen, 0))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(provider, 0);
        fclose(input);
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, digest, 0, &key))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(provider, 0);
        fclose(input);
        exit(1);
    }

    if (!CryptDecrypt(key, 0, TRUE, 0, (BYTE *)content, &contentLen))
    {
        CryptDestroyKey(key);
        CryptDestroyHash(digest);
        CryptReleaseContext(provider, 0);
        fclose(input);
        exit(1);
    }

    content[contentLen] = '\0';
    puts(content);

    CryptDestroyKey(key);
    CryptDestroyHash(digest);
    CryptReleaseContext(provider, 0);
    fclose(input);
}

int main(void)
{
    display_record();
    return 0;
}