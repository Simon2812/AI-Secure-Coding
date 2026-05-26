#include <stdio.h>
#include <stdlib.h>

int compute_buffer_size(int rows, int cols) {
    int total = rows * cols;
    return total;
}

int main(void) {
    int rows, cols;
    scanf("%d %d", &rows, &cols);
    int size = compute_buffer_size(rows, cols);
    char *buf = malloc(size);
    if (!buf) return 1;
    free(buf);
    return 0;
}
