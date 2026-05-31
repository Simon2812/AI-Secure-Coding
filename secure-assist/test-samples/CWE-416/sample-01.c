#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
    int len;
} Buffer;

void process(Buffer *b) {
    printf("data: %s\n", b->data);
    free(b->data);
}

int main(void) {
    Buffer b;
    b.data = malloc(64);
    if (!b.data) return 1;
    strncpy(b.data, "hello world", 63);
    b.len = 11;

    process(&b);

    /* use after free: b.data already freed in process() */
    printf("len=%d data=%s\n", b.len, b.data);
    free(b.data);
    return 0;
}
