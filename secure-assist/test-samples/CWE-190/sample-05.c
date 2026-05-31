#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

void process(int len) {
    int adjusted = len + 8;
    char *buf = malloc(adjusted);
    if (!buf) return;
    free(buf);
}

int main(void) {
    int length;
    scanf("%d", &length);
    process(length);
    return 0;
}
