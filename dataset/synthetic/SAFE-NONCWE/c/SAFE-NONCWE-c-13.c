#include <stdio.h>

unsigned int set_flag(unsigned int flags, unsigned int mask) {
    return flags | mask;
}

unsigned int clear_flag(unsigned int flags, unsigned int mask) {
    return flags & (~mask);
}

unsigned int toggle_flag(unsigned int flags, unsigned int mask) {
    return flags ^ mask;
}

int is_flag_set(unsigned int flags, unsigned int mask) {
    return (flags & mask) != 0;
}

void print_bits(unsigned int value) {
    int i;
    for (i = 31; i >= 0; --i) {
        putchar((value & (1u << i)) ? '1' : '0');
        if (i % 8 == 0 && i != 0) {
            putchar(' ');
        }
    }
    putchar('\n');
}

int main(void) {
    unsigned int flags = 0;

    flags = set_flag(flags, 1u << 1);   // set bit 1
    flags = set_flag(flags, 1u << 4);   // set bit 4
    flags = toggle_flag(flags, 1u << 1); // toggle bit 1
    flags = set_flag(flags, 1u << 7);   // set bit 7

    print_bits(flags);

    if (is_flag_set(flags, 1u << 4)) {
        puts("Flag 4 is active");
    }

    flags = clear_flag(flags, 1u << 4);

    print_bits(flags);

    return 0;
}