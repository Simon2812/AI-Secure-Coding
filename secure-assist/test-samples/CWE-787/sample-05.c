#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n;
    scanf("%d", &n);

    int buf[8];
    for (int i = 0; i < n; i++) {
        buf[i] = i;
    }

    for (int i = 0; i < 8; i++) printf("%d ", buf[i]);
    printf("\n");
    return 0;
}
