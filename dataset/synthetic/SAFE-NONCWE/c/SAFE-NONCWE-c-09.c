#include <stdio.h>

void rotate_clockwise(int src[3][3], int dst[3][3]) {
    int i, j;

    for (i = 0; i < 3; ++i) {
        for (j = 0; j < 3; ++j) {
            dst[j][2 - i] = src[i][j];
        }
    }
}

void print_matrix(int m[3][3]) {
    int i, j;

    for (i = 0; i < 3; ++i) {
        for (j = 0; j < 3; ++j) {
            printf("%d ", m[i][j]);
        }
        printf("\n");
    }
}

int main(void) {
    int original[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    int rotated[3][3];

    rotate_clockwise(original, rotated);

    printf("Original:\n");
    print_matrix(original);

    printf("\nRotated:\n");
    print_matrix(rotated);

    return 0;
}