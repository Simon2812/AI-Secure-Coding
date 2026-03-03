#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>   

#define MAX_QUERY 128

typedef struct {
    char filter[MAX_QUERY];
    int limit;
} LogQuery;

static void trim_newline(char *s) {
    size_t n = strlen(s);
    if (n > 0 && s[n - 1] == '\n') {
        s[n - 1] = '\0';
    }
}

static int execute_search(const LogQuery *q) {
    char cmd[256];

    snprintf(cmd, sizeof(cmd), "grep '%s' /var/log/syslog", q->filter);

    FILE *fp = popen(cmd, "r");
    if (!fp) {
        perror("popen");
        return -1;
    }

    char line[256];
    int count = 0;
    while (count < q->limit && fgets(line, sizeof(line), fp)) {
        fputs(line, stdout);
        count++;
    }

    pclose(fp);
    return 0;
}

static int handle_query(const char *user_input) {
    LogQuery q;
    memset(&q, 0, sizeof(q));

    strncpy(q.filter, user_input, sizeof(q.filter) - 1);
    trim_newline(q.filter);

    q.limit = 10;

    fprintf(stderr, "[req:%ld] searching logs...\n", (long)getpid());
    return execute_search(&q);
}

int main(void) {
    char input[MAX_QUERY];

    printf("Enter log filter: ");
    if (!fgets(input, sizeof(input), stdin)) {
        return 1;
    }

    if (input[0] == '\n' || input[0] == '\0') {
        fprintf(stderr, "Empty filter\n");
        return 1;
    }

    return handle_query(input);
}