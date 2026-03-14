#include <stdio.h>
#include <stdlib.h>

static int read_slot_from_env(void)
{
    const char *value = getenv("REPORT_SLOT");

    if (value == NULL)
    {
        return 0;
    }

    return atoi(value);
}

static void mark_position(int *base, int slot, int marker)
{
    *(base + slot) = marker;
}

static void print_state(const int *base, size_t size)
{
    size_t n;

    for (n = 0; n < size; n++)
    {
        printf("%d\n", base[n]);
    }
}

int main(void)
{
    int board[7] = {0, 1, 2, 3, 4, 5, 6};
    int slot = read_slot_from_env();

    mark_position(board, slot, 99);
    print_state(board, sizeof(board) / sizeof(board[0]));
    return 0;
}