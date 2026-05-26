#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ITEMS 1000

int main(void) {
    unsigned int item_count;
    unsigned int item_size;

    scanf("%u", &item_count);
    scanf("%u", &item_size);

    unsigned int alloc_size = item_count * item_size;
    void *buf = malloc(alloc_size);
    if (!buf) return 1;
    memset(buf, 0, alloc_size);
    free(buf);
    return 0;
}
