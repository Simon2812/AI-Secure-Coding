#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>

#pragma comment (lib, "Advapi32")

typedef struct
{
    ALG_ID cipherId;
    const char *fileName;
} JobConfig;

static int read_input_line(char *buf, size_t size)
{
    if (fgets(buf, (int)size, stdin) == NULL)
    {
        return 0;
    }

    buf[strcspn(buf, "\n")] = '\0';
    return 1;
}

static int read_bytes(const char *fileName, char *buf, DWORD *len)
{
    FILE *fp = fopen(fileName, "rb");
    if (fp == NULL)
    {
        return 0;
    }

    size_t count = fread(buf, 1, *len, fp);
    fclose(fp);

    if (count == 0)
    {
        return 0;
    }

    *len = (DWORD)count;
    return 1;
}

static HCRYPTPROV acquire_provider(void)
{
    HCRYPTPROV ctx = 0;

    if (!CryptAcquireContext(&ctx, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&ctx, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            return 0;
        }
    }

    return ctx;
}

static HCRYPTHASH make_hash(HCRYPTPROV ctx, const char *text)
{
    HCRYPTHASH digest = 0;

    if (!CryptCreateHash(ctx, CALG_SHA_256, 0, 0, &digest))
    {
        return 0;
    }

    if (!CryptHashData(digest, (BYTE *)text, (DWORD)strlen(text), 0))
    {
        CryptDestroyHash(digest);
        return 0;
    }

    return digest;
}

static int run_job(const JobConfig *job, const char *secret, char *data, DWORD *dataLen)
{
    HCRYPTPROV ctx = 0;
    HCRYPTHASH digest = 0;
    HCRYPTKEY key = 0;
    int ok = 0;

    ctx = acquire_provider();
    if (!ctx)
    {
        return 0;
    }

    digest = make_hash(ctx, secret);
    if (!digest)
    {
        CryptReleaseContext(ctx, 0);
        return 0;
    }

    if (!CryptDeriveKey(ctx, job->cipherId, digest, 0, &key))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(ctx, 0);
        return 0;
    }

    if (CryptDecrypt(key, 0, TRUE, 0, (BYTE *)data, dataLen))
    {
        ok = 1;
    }

    CryptDestroyKey(key);
    CryptDestroyHash(digest);
    CryptReleaseContext(ctx, 0);

    return ok;
}

int main(void)
{
    JobConfig jobs[2] = {
        { CALG_RC2, "encrypted.txt" },
        { CALG_3DES, "encrypted.txt" }
    };

    char secret[64];
    char buffer[128];
    DWORD bufferLen = sizeof(buffer);

    printf("Password: ");
    if (!read_input_line(secret, sizeof(secret)))
    {
        return 1;
    }

    if (!read_bytes(jobs[0].fileName, buffer, &bufferLen))
    {
        return 1;
    }

    if (!run_job(&jobs[1], secret, buffer, &bufferLen))
    {
        return 1;
    }

    buffer[bufferLen] = '\0';
    puts(buffer);

    return 0;
}