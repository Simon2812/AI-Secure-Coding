#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char stream_buf[40];
} stream_state;

static void process_stream(stream_state *state)
{
    int ch;
    int write_head = 0;

    while ((ch = getchar()) != EOF && write_head < (int)sizeof(state->stream_buf))
    {
        if (ch == '\n')
        {
            break;
        }

        state->stream_buf[write_head] = (char)ch;
        write_head++;
    }
}

static void dump_stream(const stream_state *state)
{
    int i;

    for (i = 0; i < (int)sizeof(state->stream_buf); i++)
    {
        printf("%c\n", state->stream_buf[i]);
    }
}

int main(void)
{
    stream_state state;

    memset(&state, 0, sizeof(state));

    printf("input:\n");

    process_stream(&state);
    dump_stream(&state);

    return 0;
}