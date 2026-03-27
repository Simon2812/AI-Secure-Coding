#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char first_target[128];
    char second_target[128];
    char label[48];
    char command_name[32];
} AuditJob;

static void init_job(AuditJob *job)
{
    strncpy(job->first_target, ".", sizeof(job->first_target) - 1);
    job->first_target[sizeof(job->first_target) - 1] = '\0';

    strncpy(job->second_target, "/tmp", sizeof(job->second_target) - 1);
    job->second_target[sizeof(job->second_target) - 1] = '\0';

    strncpy(job->label, "audit-", sizeof(job->label) - 1);
    job->label[sizeof(job->label) - 1] = '\0';

    strncpy(job->command_name, "ls", sizeof(job->command_name) - 1);
    job->command_name[sizeof(job->command_name) - 1] = '\0';
}

static void load_job(AuditJob *job, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(job->first_target, argv[1], sizeof(job->first_target) - 1);
        job->first_target[sizeof(job->first_target) - 1] = '\0';
    }

    if (argc > 2)
    {
        strncpy(job->second_target, argv[2], sizeof(job->second_target) - 1);
        job->second_target[sizeof(job->second_target) - 1] = '\0';
    }

    if (argc > 3)
    {
        strncpy(job->command_name, argv[3], sizeof(job->command_name) - 1);
        job->command_name[sizeof(job->command_name) - 1] = '\0';
    }

    if (argc > 4)
    {
        size_t base = strlen(job->label);
        size_t i = 0;

        while (argv[4][i] != '\0')
        {
            job->label[base + i] = argv[4][i];
            i++;
        }

        job->label[base + i] = '\0';
    }
}

static void print_job(const AuditJob *job)
{
    printf("Label: %s\n", job->label);
    printf("Primary: %s\n", job->first_target);
    printf("Secondary: %s\n", job->second_target);
    printf("Command: %s\n", job->command_name);
}

static void run_primary(const char *target)
{
    char command[256] = "find ";
    strncat(command, target, sizeof(command) - strlen(command) - 1);
    strncat(command, " -maxdepth 1", sizeof(command) - strlen(command) - 1);
    system(command);
}

static void run_secondary(const char *command_name, const char *target)
{
    execlp(command_name, command_name, target, (char *)NULL);
}

static void run_constant_check(void)
{
    system("pwd");
}

int main(int argc, char *argv[])
{
    AuditJob job;

    init_job(&job);
    load_job(&job, argc, argv);

    print_job(&job);
    run_constant_check();
    run_primary(job.first_target);
    run_secondary(job.command_name, job.second_target);

    return 0;
}