#include <stdio.h>
#include <ctype.h>

void to_lowercase(char *s) {
    while (*s) {
        *s = (char)tolower((unsigned char)*s);
        s++;
    }
}

void collapse_spaces(char *s) {
    char *read = s;
    char *write = s;
    int in_space = 0;

    while (*read) {
        if (isspace((unsigned char)*read)) {
            if (!in_space) {
                *write++ = ' ';
                in_space = 1;
            }
        } else {
            *write++ = *read;
            in_space = 0;
        }
        read++;
    }

    if (write > s && *(write - 1) == ' ') {
        write--;
    }

    *write = '\0';
}

void capitalize_words(char *s) {
    int new_word = 1;

    while (*s) {
        if (isspace((unsigned char)*s)) {
            new_word = 1;
        } else if (new_word) {
            *s = (char)toupper((unsigned char)*s);
            new_word = 0;
        }
        s++;
    }
}

int main(void) {
    char text[] = "   HeLLo   WoRLd   FROM   C   ";

    to_lowercase(text);
    collapse_spaces(text);
    capitalize_words(text);

    printf("%s\n", text);

    return 0;
}