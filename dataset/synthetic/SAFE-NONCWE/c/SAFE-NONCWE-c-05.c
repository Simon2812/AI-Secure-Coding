#include <stdio.h>
#include <ctype.h>
#include <string.h>

int is_palindrome(const char *text) {
    const char *left = text;
    const char *right = text + strlen(text);

    if (right == text) {
        return 1;
    }

    right--;

    while (left < right) {
        while (left < right && !isalnum((unsigned char)*left)) {
            left++;
        }

        while (left < right && !isalnum((unsigned char)*right)) {
            right--;
        }

        if (tolower((unsigned char)*left) != tolower((unsigned char)*right)) {
            return 0;
        }

        left++;
        right--;
    }

    return 1;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        puts("Provide a string as argument");
        return 1;
    }

    if (is_palindrome(argv[1])) {
        puts("Yes");
    } else {
        puts("No");
    }

    return 0;
}