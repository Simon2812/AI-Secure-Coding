#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void copy_data(int count, const char *src) {
    char *dst = malloc(count + 1);
    if (!dst) return;
    memcpy(dst, src, count + 1);
    printf("%s\n", dst);
    free(dst);
}

int main(void) {
    int n;
    scanf("%d", &n);
    copy_data(n, "hello");
    return 0;
}
