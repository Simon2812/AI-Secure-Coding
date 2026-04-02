#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char algorithm[16];
    char hash_name[16];
    char label[32];
} CryptoJob;

static void init_job(CryptoJob *job)
{
    strncpy(job->algorithm, "DES", sizeof(job->algorithm) - 1);
    job->algorithm[sizeof(job->algorithm) - 1] = '\0';

    strncpy(job->hash_name, "MD5", sizeof(job->hash_name) - 1);
    job->hash_name[sizeof(job->hash_name) - 1] = '\0';

    strncpy(job->label, "task", sizeof(job->label) - 1);
    job->label[sizeof(job->label) - 1] = '\0';
}

static void load_job(CryptoJob *job, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(job->label, argv[1], sizeof(job->label) - 1);
        job->label[sizeof(job->label) - 1] = '\0';
    }
}

static void print_job(const CryptoJob *job)
{
    printf("Label: %s\n", job->label);
    printf("Algorithm: %s\n", job->algorithm);
    printf("Hash: %s\n", job->hash_name);
}

static void format_output(const CryptoJob *job)
{
    char buffer[128];

    snprintf(buffer, sizeof(buffer), "[%s] %s/%s",
             job->label, job->algorithm, job->hash_name);

    printf("%s\n", buffer);
}

int main(int argc, char *argv[])
{
    CryptoJob job;

    init_job(&job);
    load_job(&job, argc, argv);

    print_job(&job);
    format_output(&job);

    return 0;
}