#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char cipher_name[24];
    char digest_name[24];
    char secret[40];
    char profile[32];
    char note[48];
} CryptoSettings;

static void init_settings(CryptoSettings *settings)
{
    strncpy(settings->cipher_name, "3DES", sizeof(settings->cipher_name) - 1);
    settings->cipher_name[sizeof(settings->cipher_name) - 1] = '\0';

    strncpy(settings->digest_name, "SHA224", sizeof(settings->digest_name) - 1);
    settings->digest_name[sizeof(settings->digest_name) - 1] = '\0';

    strncpy(settings->secret, "p8M2x4Qn7Lz1Rw5T", sizeof(settings->secret) - 1);
    settings->secret[sizeof(settings->secret) - 1] = '\0';

    strncpy(settings->profile, "default", sizeof(settings->profile) - 1);
    settings->profile[sizeof(settings->profile) - 1] = '\0';

    strncpy(settings->note, "ready", sizeof(settings->note) - 1);
    settings->note[sizeof(settings->note) - 1] = '\0';
}

static void load_settings(CryptoSettings *settings, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(settings->profile, argv[1], sizeof(settings->profile) - 1);
        settings->profile[sizeof(settings->profile) - 1] = '\0';
    }

    if (argc > 2)
    {
        strncpy(settings->note, argv[2], sizeof(settings->note) - 1);
        settings->note[sizeof(settings->note) - 1] = '\0';
    }
}

static void read_secret(CryptoSettings *settings)
{
    FILE *file = fopen("app.key", "r");
    if (file != NULL)
    {
        if (fgets(settings->secret, sizeof(settings->secret), file) != NULL)
        {
            settings->secret[strcspn(settings->secret, "\r\n")] = '\0';
        }
        fclose(file);
    }
}

static void print_settings(const CryptoSettings *settings)
{
    printf("Profile: %s\n", settings->profile);
    printf("Cipher: %s\n", settings->cipher_name);
    printf("Digest: %s\n", settings->digest_name);
    printf("Secret length: %zu\n", strlen(settings->secret));
    printf("Note: %s\n", settings->note);
}

static void build_line(const CryptoSettings *settings)
{
    char line[160];

    snprintf(line, sizeof(line), "%s|%s|%s",
             settings->profile, settings->cipher_name, settings->digest_name);

    printf("%s\n", line);
}

int main(int argc, char *argv[])
{
    CryptoSettings settings;

    init_settings(&settings);
    load_settings(&settings, argc, argv);
    read_secret(&settings);

    print_settings(&settings);
    build_line(&settings);

    return 0;
}