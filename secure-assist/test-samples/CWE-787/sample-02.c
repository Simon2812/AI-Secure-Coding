#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    int *arr = malloc(10 * sizeof(int));
    if (!arr) return 1;

    for (int i = 0; i <= 10; i++) {
        arr[i] = i * i;
    }

    for (int i = 0; i < 10; i++) printf("%d ", arr[i]);
    printf("\n");
    free(arr);
    return 0;
}
