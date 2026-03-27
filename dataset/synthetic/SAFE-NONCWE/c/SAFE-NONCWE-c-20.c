#include <stdio.h>
#include <string.h>
#include <ctype.h>

int check_length(const char *s, int min, int max) {
    size_t len = strlen(s);
    return len >= (size_t)min && len <= (size_t)max;
}

int has_digit(const char *s) {
    while (*s) {
        if (isdigit((unsigned char)*s)) {
            return 1;
        }
        s++;
    }
    return 0;
}

int has_letter(const char *s) {
    while (*s) {
        if (isalpha((unsigned char)*s)) {
            return 1;
        }
        s++;
    }
    return 0;
}

int has_no_spaces(const char *s) {
    while (*s) {
        if (isspace((unsigned char)*s)) {
            return 0;
        }
        s++;
    }
    return 1;
}

int validate_username(const char *username) {
    if (!check_length(username, 3, 20)) {
        return 0;
    }

    if (!has_letter(username)) {
        return 0;
    }

    if (!has_no_spaces(username)) {
        return 0;
    }

    return 1;
}

int validate_code(const char *code) {
    if (!check_length(code, 4, 8)) {
        return 0;
    }

    if (!has_digit(code)) {
        return 0;
    }

    return 1;
}

void run_validation(const char *username, const char *code) {
    int user_ok = validate_username(username);
    int code_ok = validate_code(code);

    printf("Username: %s -> %s\n", username, user_ok ? "OK" : "INVALID");
    printf("Code: %s -> %s\n", code, code_ok ? "OK" : "INVALID");

    if (user_ok && code_ok) {
        puts("Access granted");
    } else {
        puts("Access denied");
    }
}

int main(void) {
    char username[64];
    char code[64];

    printf("Enter username: ");
    if (!fgets(username, sizeof(username), stdin)) {
        return 1;
    }

    printf("Enter code: ");
    if (!fgets(code, sizeof(code), stdin)) {
        return 1;
    }

    size_t len;

    len = strlen(username);
    if (len > 0 && username[len - 1] == '\n') {
        username[len - 1] = '\0';
    }

    len = strlen(code);
    if (len > 0 && code[len - 1] == '\n') {
        code[len - 1] = '\0';
    }

    run_validation(username, code);

    return 0;
}