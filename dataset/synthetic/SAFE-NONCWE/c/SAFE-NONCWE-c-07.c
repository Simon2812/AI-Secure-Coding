#include <stdio.h>

int is_even(int x) {
    return x % 2 == 0;
}

int is_positive(int x) {
    return x > 0;
}

int greater_than_ten(int x) {
    return x > 10;
}

int square(int x) {
    return x * x;
}

int increment(int x) {
    return x + 1;
}

int process(int value, int (*filter)(int), int (*transform)(int)) {
    if (filter(value)) {
        return transform(value);
    }
    return value;
}

int main(void) {
    int values[] = {3, -2, 7, 12, 0, 5, 20};
    int count = sizeof(values) / sizeof(values[0]);
    int i;

    int (*filter_fn)(int) = is_positive;
    int (*transform_fn)(int) = square;

    for (i = 0; i < count; ++i) {
        int result = process(values[i], filter_fn, transform_fn);
        printf("%d -> %d\n", values[i], result);
    }

    return 0;
}