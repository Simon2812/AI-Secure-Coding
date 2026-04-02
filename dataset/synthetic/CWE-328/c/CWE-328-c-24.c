#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define SIZE 128
#define LEN (512 / 8)

static int verify(const char *input, const UCHAR *expected)
{
    HCRYPTPROV ctx = 0;
    HCRYPTHASH h = 0;
    UCHAR *out = (UCHAR*)malloc(LEN);
    DWORD s = LEN;
    int result = 0;

    if (!out) return 0;

    if (!CryptAcquireContextW(&ctx, NULL, NULL, PROV_RSA_FULL, 0))
        goto end;

    if (!CryptCreateHash(ctx, CALG_SHA_512, 0, 0, &h))
        goto end;

    if (!CryptHashData(h, (BYTE*)input, (DWORD)strlen(input), 0))
        goto end;

    if (!CryptGetHashParam(h, HP_HASHVAL, out, &s, 0))
        goto end;

    result = (memcmp(out, expected, LEN) == 0);

end:
    if (h) CryptDestroyHash(h);
    if (ctx) CryptReleaseContext(ctx, 0);
    free(out);
    return result;
}

int main(void)
{
    FILE *f = fopen("password.txt", "r");
    UCHAR ref[LEN];
    char buf[SIZE];
    size_t i;

    if (!f) return 1;

    for (i = 0; i < LEN; i++)
    {
        ULONG v;
        if (fscanf(f, "%02x", &v) != 1 || v > 0xff)
        {
            fclose(f);
            return 1;
        }
        ref[i] = (UCHAR)v;
    }
    fclose(f);

    if (!fgets(buf, sizeof(buf), stdin))
        return 1;

    buf[strcspn(buf, "\r\n")] = 0;

    puts(verify(buf, ref) ? "OK" : "FAIL");
    return 0;
}