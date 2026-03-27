#include <stdio.h>
#include <stdlib.h>

void normalize_time(int *h, int *m, int *s) {
    if (*s >= 60) {
        *m += *s / 60;
        *s %= 60;
    }

    if (*m >= 60) {
        *h += *m / 60;
        *m %= 60;
    }

    if (*s < 0) {
        int borrow = (-*s + 59) / 60;
        *m -= borrow;
        *s += borrow * 60;
    }

    if (*m < 0) {
        int borrow = (-*m + 59) / 60;
        *h -= borrow;
        *m += borrow * 60;
    }

    if (*h < 0) {
        *h = 0;
        *m = 0;
        *s = 0;
    }
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        puts("Usage: <hours> <minutes> <seconds>");
        return 1;
    }

    int h = atoi(argv[1]);
    int m = atoi(argv[2]);
    int s = atoi(argv[3]);

    normalize_time(&h, &m, &s);

    printf("%02d:%02d:%02d\n", h, m, s);
    return 0;
}