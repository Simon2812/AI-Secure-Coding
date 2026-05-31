#include <stdio.h>
#include <string.h>

void parse_input(const char *input) {
    char token[32];
    int idx = 0;
    for (int i = 0; input[i] != '\0'; i++) {
        token[idx++] = input[i];
    }
    token[idx] = '\0';
    printf("token: %s\n", token);
}

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    parse_input(argv[1]);
    return 0;
}
