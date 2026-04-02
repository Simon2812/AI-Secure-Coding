#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

typedef struct
{
    const char *path;
    ALG_ID algorithm;
} Request;

static int read_payload(const Request *req, char *buffer, DWORD *length)
{
    FILE *fp = fopen(req->path, "rb");
    if (fp == NULL)
    {
        return 0;
    }

    size_t used = fread(buffer, 1, *length, fp);
    fclose(fp);

    if (used == 0)
    {
        return 0;
    }

    *length = (DWORD)used;
    return 1;
}

static int unlock_text(const Request *req, const char *secret, char *buffer, DWORD *length)
{
    HCRYPTPROV provider = 0;
    HCRYPTHASH digest = 0;
    HCRYPTKEY key = 0;
    int status = 0;

    if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            return 0;
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &digest))
    {
        CryptReleaseContext(provider, 0);
        return 0;
    }

    if (!CryptHashData(digest, (BYTE *)secret, (DWORD)strlen(secret), 0))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(provider, 0);
        return 0;
    }

    if (!CryptDeriveKey(provider, req->algorithm, digest, 0, &key))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(provider, 0);
        return 0;
    }

    if (CryptDecrypt(key, 0, TRUE, 0, (BYTE *)buffer, length))
    {
        status = 1;
    }

    CryptDestroyKey(key);
    CryptDestroyHash(digest);
    CryptReleaseContext(provider, 0);

    return status;
}

int main(void)
{
    Request req = { "encrypted.txt", CALG_AES_256 };
    char password[72];
    char payload[128];
    DWORD payloadLen = sizeof(payload);

    printf("Secret: ");
    if (fgets(password, sizeof(password), stdin) == NULL)
    {
        return 1;
    }

    password[strcspn(password, "\n")] = '\0';

    if (!read_payload(&req, payload, &payloadLen))
    {
        return 1;
    }

    if (!unlock_text(&req, password, payload, &payloadLen))
    {
        return 1;
    }

    payload[payloadLen] = '\0';
    puts(payload);

    return 0;
}