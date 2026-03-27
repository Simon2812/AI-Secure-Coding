#include <stdio.h>
#include <ctype.h>

int main(void) {
    int ch;
    int current = 0;
    int sign = 1;
    int in_number = 0;
    long total = 0;

    while ((ch = getchar()) != EOF) {
        if (ch == '-') {
            if (!in_number) {
                sign = -1;
                in_number = 1;
                current = 0;
            } else {
                total += sign * current;
                sign = -1;
                current = 0;
            }
        } else if (isdigit(ch)) {
            if (!in_number) {
                in_number = 1;
                sign = 1;
                current = 0;
            }
            current = current * 10 + (ch - '0');
        } else {
            if (in_number) {
                total += sign * current;
                in_number = 0;
                current = 0;
                sign = 1;
            }
        }
    }

    if (in_number) {
        total += sign * current;
    }

    printf("%ld\n", total);
    return 0;
}