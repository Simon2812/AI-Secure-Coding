#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char *buffer;
    size_t size;
} DataBlock;

static DataBlock *create_block(const char *input)
{
    DataBlock *block = (DataBlock *)malloc(sizeof(DataBlock));
    if (block == NULL)
    {
        return NULL;
    }

    block->size = strlen(input) + 1;
    block->buffer = (char *)malloc(block->size);

    if (block->buffer == NULL)
    {
        free(block);
        return NULL;
    }

    strncpy(block->buffer, input, block->size - 1);
    block->buffer[block->size - 1] = '\0';

    return block;
}

static void release_block(DataBlock *block)
{
    if (block == NULL)
    {
        return;
    }

    if (block->buffer != NULL)
    {
        free(block->buffer);
    }

    free(block);
}

static void print_block(const DataBlock *block)
{
    if (block != NULL && block->buffer != NULL)
    {
        printf("Content: %s\n", block->buffer);
    }
}

static void process_input(const char *input)
{
    DataBlock *block = create_block(input);

    if (block == NULL)
    {
        return;
    }

    print_block(block);

    release_block(block);

    if (block->buffer != NULL)
    {
        printf("After free: %s\n", block->buffer);
    }
}

int main(int argc, char *argv[])
{
    const char *input = "default";

    if (argc > 1)
    {
        input = argv[1];
    }

    process_input(input);

    return 0;
}