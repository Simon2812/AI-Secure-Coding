#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char cipher[16];
    char input[128];
} Job;

static void init_job(Job *j)
{
    strncpy(j->cipher, "RC4", sizeof(j->cipher) - 1);
    j->cipher[sizeof(j->cipher) - 1] = '\0';

    strncpy(j->input, "data", sizeof(j->input) - 1);
    j->input[sizeof(j->input) - 1] = '\0';
}

static void encrypt_block(const char *cipher, const char *data)
{
    printf("Encrypt (%s): %s\n", cipher, data);
}

static void log_cipher(const char *cipher)
{
    printf("Using cipher: %s\n", cipher);
}

static void exec_info(void)
{
    system("date");
}

static void memory_op(void)
{
    char *tmp = (char *)malloc(32);
    if (tmp != NULL)
    {
        strcpy(tmp, "ok");
        printf("%s\n", tmp);
        free(tmp);
    }
}

int main(int argc, char *argv[])
{
    Job j;

    init_job(&j);

    encrypt_block(j.cipher, j.input);
    log_cipher(j.cipher);

    exec_info();
    memory_op();

    return 0;
}