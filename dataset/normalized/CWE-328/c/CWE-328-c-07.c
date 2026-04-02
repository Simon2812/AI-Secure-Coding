#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define TEXT_LIMIT 128
#define TOKEN_SIZE (128 / 8)

static int fetch_digest(UCHAR *target, size_t width)
{
    FILE *source = fopen("password.txt", "r");
    size_t pos = 0;

    if (source == NULL)
    {
        return 0;
    }

    while (pos < width)
    {
        ULONG piece;
        if (fscanf(source, "%02x", &piece) != 1 || piece > 0xff)
        {
            fclose(source);
            return 0;
        }
        target[pos++] = (UCHAR)piece;
    }

    fclose(source);
    return 1;
}

static void drop_newline(char *text)
{
    size_t n = strcspn(text, "\r\n");
    text[n] = '\0';
}

int main(void)
{
    HCRYPTPROV session = 0;
    HCRYPTHASH digest = 0;
    char secret[TEXT_LIMIT];
    UCHAR baseline[TOKEN_SIZE];
    UCHAR current[TOKEN_SIZE];
    DWORD currentSize = TOKEN_SIZE;

    if (!fetch_digest(baseline, TOKEN_SIZE))
    {
        return 1;
    }

    if (fgets(secret, sizeof(secret), stdin) == NULL)
    {
        return 1;
    }

    drop_newline(secret);

    if (!CryptAcquireContextW(&session, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 1;
    }

    if (!CryptCreateHash(session, CALG_MD2, 0, 0, &digest))
    {
        CryptReleaseContext(session, 0);
        return 1;
    }

    if (!CryptHashData(digest, (BYTE *)secret, (DWORD)strlen(secret), 0))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(session, 0);
        return 1;
    }

    if (!CryptGetHashParam(digest, HP_HASHVAL, (BYTE *)current, &currentSize, 0))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(session, 0);
        return 1;
    }

    puts(memcmp(baseline, current, TOKEN_SIZE * sizeof(UCHAR)) == 0 ? "Access granted" : "Access denied");

    CryptDestroyHash(digest);
    CryptReleaseContext(session, 0);
    return 0;
}