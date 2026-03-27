#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char key[32];
    char algorithm[16];
    char hash_name[16];
    char label[32];
} CryptoProfile;

static void init_profile(CryptoProfile *p)
{
    strncpy(p->key, "k9f3L2x8Qw7Zp4Mn", sizeof(p->key) - 1);
    p->key[sizeof(p->key) - 1] = '\0';

    strncpy(p->algorithm, "RC4", sizeof(p->algorithm) - 1);
    p->algorithm[sizeof(p->algorithm) - 1] = '\0';

    strncpy(p->hash_name, "SHA1", sizeof(p->hash_name) - 1);
    p->hash_name[sizeof(p->hash_name) - 1] = '\0';

    strncpy(p->label, "profile", sizeof(p->label) - 1);
    p->label[sizeof(p->label) - 1] = '\0';
}

static void load_profile(CryptoProfile *p, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(p->label, argv[1], sizeof(p->label) - 1);
        p->label[sizeof(p->label) - 1] = '\0';
    }
}

static void print_profile(const CryptoProfile *p)
{
    printf("Label: %s\n", p->label);
    printf("Algorithm: %s\n", p->algorithm);
    printf("Hash: %s\n", p->hash_name);
    printf("Key length: %zu\n", strlen(p->key));
}

static void format_line(const CryptoProfile *p)
{
    char buffer[128];

    snprintf(buffer, sizeof(buffer), "%s:%s:%s",
             p->label, p->algorithm, p->hash_name);

    printf("%s\n", buffer);
}

int main(int argc, char *argv[])
{
    CryptoProfile profile;

    init_profile(&profile);
    load_profile(&profile, argc, argv);

    print_profile(&profile);
    format_line(&profile);

    return 0;
}