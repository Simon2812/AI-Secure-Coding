#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_DOCS 5
#define MAX_WORDS 64
#define WORD_LEN 32

typedef struct {
    char word[WORD_LEN];
    int count;
} WordEntry;

typedef struct {
    char name[32];
    WordEntry words[MAX_WORDS];
    int word_count;
} Document;

void to_lowercase(char *s) {
    while (*s) {
        *s = (char)tolower((unsigned char)*s);
        s++;
    }
}

void clean_word(char *w) {
    int i, j = 0;
    for (i = 0; w[i]; ++i) {
        if (isalnum((unsigned char)w[i])) {
            w[j++] = (char)tolower((unsigned char)w[i]);
        }
    }
    w[j] = '\0';
}

int find_word(WordEntry words[], int count, const char *w) {
    int i;
    for (i = 0; i < count; ++i) {
        if (strcmp(words[i].word, w) == 0) {
            return i;
        }
    }
    return -1;
}

void add_word(Document *doc, const char *w) {
    if (w[0] == '\0') {
        return;
    }

    int idx = find_word(doc->words, doc->word_count, w);

    if (idx >= 0) {
        doc->words[idx].count++;
    } else if (doc->word_count < MAX_WORDS) {
        snprintf(doc->words[doc->word_count].word, WORD_LEN, "%s", w);
        doc->words[doc->word_count].count = 1;
        doc->word_count++;
    }
}

void index_text(Document *doc, char text[]) {
    char *token = strtok(text, " ");
    while (token) {
        clean_word(token);
        add_word(doc, token);
        token = strtok(NULL, " ");
    }
}

int score_document(const Document *doc, const char *query) {
    int i;
    int score = 0;

    for (i = 0; i < doc->word_count; ++i) {
        if (strcmp(doc->words[i].word, query) == 0) {
            score += doc->words[i].count;
        }
    }

    return score;
}

void print_index(const Document *doc) {
    int i;
    printf("Index for %s:\n", doc->name);

    for (i = 0; i < doc->word_count; ++i) {
        printf("  %s: %d\n", doc->words[i].word, doc->words[i].count);
    }
}

void search(const Document docs[], int count, const char *query) {
    int i;
    int best = -1;
    int best_score = 0;

    for (i = 0; i < count; ++i) {
        int s = score_document(&docs[i], query);
        printf("Doc %s score: %d\n", docs[i].name, s);

        if (s > best_score) {
            best_score = s;
            best = i;
        }
    }

    if (best >= 0) {
        printf("Best match: %s\n", docs[best].name);
    } else {
        printf("No matches found\n");
    }
}

int main(void) {
    Document docs[MAX_DOCS] = {
        {"doc1", {}, 0},
        {"doc2", {}, 0},
        {"doc3", {}, 0}
    };

    char text1[] = "Apple banana apple orange";
    char text2[] = "Banana fruit banana apple";
    char text3[] = "Orange fruit citrus";

    index_text(&docs[0], text1);
    index_text(&docs[1], text2);
    index_text(&docs[2], text3);

    int i;
    for (i = 0; i < 3; ++i) {
        print_index(&docs[i]);
    }

    char query[WORD_LEN] = "apple";
    to_lowercase(query);

    printf("\nSearch results for '%s':\n", query);
    search(docs, 3, query);

    return 0;
}