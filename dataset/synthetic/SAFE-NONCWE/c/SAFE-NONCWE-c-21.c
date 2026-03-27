#include <stdio.h>
#include <string.h>

int add(int a, int b) {
    return a + b;
}

int sub(int a, int b) {
    return a - b;
}

int mul(int a, int b) {
    return a * b;
}

int max(int a, int b) {
    return (a > b) ? a : b;
}

typedef int (*operation_fn)(int, int);

operation_fn resolve_operation(const char *name) {
    if (strcmp(name, "add") == 0) {
        return add;
    } else if (strcmp(name, "sub") == 0) {
        return sub;
    } else if (strcmp(name, "mul") == 0) {
        return mul;
    } else if (strcmp(name, "max") == 0) {
        return max;
    }

    return NULL;
}

int execute(const char *op_name, int a, int b, int *result) {
    operation_fn fn = resolve_operation(op_name);

    if (!fn) {
        return 0;
    }

    *result = fn(a, b);
    return 1;
}

int main(void) {
    char command[32];
    int a, b;
    int result;

    while (1) {
        printf("Enter command (add/sub/mul/max/exit): ");

        if (!fgets(command, sizeof(command), stdin)) {
            break;
        }

        size_t len = strlen(command);
        if (len > 0 && command[len - 1] == '\n') {
            command[len - 1] = '\0';
        }

        if (strcmp(command, "exit") == 0) {
            break;
        }

        printf("Enter two integers: ");
        if (scanf("%d %d", &a, &b) != 2) {
            puts("Invalid input");
            return 1;
        }

        /* consume leftover newline */
        int c;
        while ((c = getchar()) != '\n' && c != EOF);

        if (execute(command, a, b, &result)) {
            printf("Result: %d\n", result);
        } else {
            puts("Unknown operation");
        }
    }

    return 0;
}