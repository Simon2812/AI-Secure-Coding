#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    unsigned char buffer[32];
} storage;

static int read_chunk_size(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static void decode_stream(storage *s, int chunk)
{
    unsigned char temp[12];
    int i;
    int write_pos = 0;

    for (i = 0; i < 12; i++)
    {
        temp[i] = (unsigned char)(i + 10);
    }

    while (chunk > 0)
    {
        for (i = 0; i < 12; i++)
        {
            s->buffer[write_pos] = temp[i];
            write_pos++;
        }

        chunk--;
    }
}

static void inspect(const storage *s)
{
    int i;

    for (i = 0; i < 32; i++)
    {
        printf("%u\n", s->buffer[i]);
    }
}

int main(void)
{
    storage s;
    int chunk;

    memset(&s, 0, sizeof(s));

    printf("chunks:\n");
    chunk = read_chunk_size();

    decode_stream(&s, chunk);
    inspect(&s);

    return 0;
}