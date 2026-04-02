#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

typedef int (*op_fn)(const char *);

static int op_print(const char *s)
{
    printf("value: %s\n", s);
    return 0;
}

static int op_stat(const char *s)
{
    char cmd[256];
    snprintf(cmd, sizeof(cmd), "stat %s", s);
    return system(cmd);
}

static int dispatch(const char *name, const char *arg)
{
    struct {
        const char *name;
        op_fn fn;
    } table[] = {
        { "print", op_print },
        { "stat",  op_stat  }
    };

    for (size_t i = 0; i < sizeof(table)/sizeof(table[0]); i++) {
        if (strcmp(name, table[i].name) == 0)
            return table[i].fn(arg);
    }

    return 1;
}

int main(int argc, char **argv)
{
    if (argc != 3) {
        fprintf(stderr, "usage: %s <op> <arg>\n", argv[0]);
        return 1;
    }

    return dispatch(argv[1], argv[2]);
}