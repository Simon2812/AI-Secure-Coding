#include <stdio.h>

int is_open(char c) {
    return c == '(' || c == '[' || c == '{';
}

int is_close(char c) {
    return c == ')' || c == ']' || c == '}';
}

int matches(char open, char close) {
    return (open == '(' && close == ')') ||
           (open == '[' && close == ']') ||
           (open == '{' && close == '}');
}

int main(void) {
    char stack[128];
    int top = 0;

    int ch;
    int valid = 1;

    while ((ch = getchar()) != EOF) {
        char c = (char)ch;

        if (c == '\n') {
            break;
        }

        if (is_open(c)) {
            if (top < (int)(sizeof(stack) / sizeof(stack[0]))) {
                stack[top++] = c;
            } else {
                valid = 0;
                break;
            }
        } else if (is_close(c)) {
            if (top == 0) {
                valid = 0;
                break;
            }

            char last = stack[top - 1];
            if (!matches(last, c)) {
                valid = 0;
                break;
            }

            top--;
        }
    }

    if (valid && top == 0) {
        puts("Balanced");
    } else {
        puts("Not balanced");
    }

    return 0;
}