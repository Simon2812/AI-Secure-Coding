#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int requested_size;
    char source[256];
} InputData;

static void read_input(InputData *data, int argc, char *argv[])
{
    data->requested_size = 32;
    strncpy(data->source, "default", sizeof(data->source) - 1);
    data->source[sizeof(data->source) - 1] = '\0';

    if (argc > 1)
    {
        data->requested_size = atoi(argv[1]);
    }

    if (argc > 2)
    {
        strncpy(data->source, argv[2], sizeof(data->source) - 1);
        data->source[sizeof(data->source) - 1] = '\0';
    }
}

static char *allocate_buffer(int size)
{
    if (size <= 0 || size > 1024)
    {
        return NULL;
    }

    return (char *)malloc(size);
}

static void process_data(char *buffer, const char *input)
{
    if (buffer == NULL)
    {
        return;
    }

    /* Potential overflow */
    strcpy(buffer, input);
}

static void print_data(const char *buffer)
{
    if (buffer != NULL)
    {
        printf("Processed: %s\n", buffer);
    }
}

int main(int argc, char *argv[])
{
    InputData data;
    char *buffer;

    read_input(&data, argc, argv);

    buffer = allocate_buffer(data.requested_size);

    process_data(buffer, data.source);

    print_data(buffer);

    free(buffer);
    return 0;
}