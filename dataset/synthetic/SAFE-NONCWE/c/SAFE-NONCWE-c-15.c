#include <stdio.h>

int is_valid_triangle(double a, double b, double c) {
    return (a + b > c) && (a + c > b) && (b + c > a);
}

int is_equilateral(double a, double b, double c) {
    return (a == b) && (b == c);
}

int is_isosceles(double a, double b, double c) {
    return (a == b) || (a == c) || (b == c);
}

double abs_val(double x) {
    return x < 0 ? -x : x;
}

double sqrt_newton(double x) {
    double guess = x > 1 ? x : 1;
    int i;

    for (i = 0; i < 20; ++i) {
        guess = 0.5 * (guess + x / guess);
    }

    return guess;
}

double triangle_area(double a, double b, double c) {
    double s = (a + b + c) / 2.0;
    double area_sq = s * (s - a) * (s - b) * (s - c);

    if (area_sq <= 0.0) {
        return 0.0;
    }

    return sqrt_newton(area_sq);
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        puts("Usage: <a> <b> <c>");
        return 1;
    }

    double a = atof(argv[1]);
    double b = atof(argv[2]);
    double c = atof(argv[3]);

    if (!is_valid_triangle(a, b, c)) {
        puts("Invalid triangle");
        return 1;
    }

    if (is_equilateral(a, b, c)) {
        puts("Equilateral");
    } else if (is_isosceles(a, b, c)) {
        puts("Isosceles");
    } else {
        puts("Scalene");
    }

    double area = triangle_area(a, b, c);
    printf("Area: %.3f\n", area);

    return 0;
}