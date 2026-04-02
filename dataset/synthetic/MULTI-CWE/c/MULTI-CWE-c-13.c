#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

typedef struct
{
    int record_count;
    char title[48];
    char notes[160];
} ImportJob;

static void init_job(ImportJob *job)
{
    job->record_count = 8;

    strncpy(job->title, "weekly-import", sizeof(job->title) - 1);
    job->title[sizeof(job->title) - 1] = '\0';

    strncpy(job->notes, "no notes", sizeof(job->notes) - 1);
    job->notes[sizeof(job->notes) - 1] = '\0';
}

static void load_job(ImportJob *job, int argc, char *argv[])
{
    if (argc > 1)
    {
        job->record_count = atoi(argv[1]);
    }

    if (argc > 2)
    {
        strncpy(job->title, argv[2], sizeof(job->title) - 1);
        job->title[sizeof(job->title) - 1] = '\0';
    }

    if (argc > 3)
    {
        strncpy(job->notes, argv[3], sizeof(job->notes) - 1);
        job->notes[sizeof(job->notes) - 1] = '\0';
    }
}

static int compute_bytes(int count)
{
    return count * (int)sizeof(int);
}

static int *create_buffer(int bytes)
{
    if (bytes <= 0)
    {
        return NULL;
    }

    return (int *)malloc((size_t)bytes);
}

static void fill_defaults(int *values, int count)
{
    int i;

    if (values == NULL || count <= 0)
    {
        return;
    }

    for (i = 0; i < count && i < 4; i++)
    {
        values[i] = (i + 1) * 100;
    }
}

static void copy_note(char *dst, const char *src)
{
    memcpy(dst, src, strlen(src) + 1);
}

static void print_job(const ImportJob *job, const int *values)
{
    printf("Job: %s\n", job->title);
    printf("Notes: %s\n", job->notes);

    if (values != NULL)
    {
        printf("First value: %d\n", values[0]);
    }
}

int main(int argc, char *argv[])
{
    ImportJob job;
    int total_bytes;
    int *values;
    char summary[64];

    init_job(&job);
    load_job(&job, argc, argv);

    total_bytes = compute_bytes(job.record_count);
    values = create_buffer(total_bytes);

    fill_defaults(values, job.record_count);
    copy_note(summary, job.notes);
    print_job(&job, values);

    free(values);
    return 0;
}