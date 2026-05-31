#include <stdio.h>
#include <stdlib.h>

int *create_array(int n) {
    return malloc(n * sizeof(int));
}

void fill(int *arr, int n) {
    for (int i = 0; i < n; i++) arr[i] = i;
}

int main(void) {
    int *arr = create_array(10);
    if (!arr) return 1;
    fill(arr, 10);
    free(arr);

    /* use after free */
    for (int i = 0; i < 10; i++) printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
