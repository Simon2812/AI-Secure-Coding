#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static int split_pair(char *s, char **a, char **b)
{
    char *p = strchr(s, ':');
    if (!p)
        return 0;
    *p = '\0';
    *a = s;
    *b = p + 1;
    return 1;
}

static int run_tool(const char *tool, const char *arg)
{
    char buf[300];
    snprintf(buf, sizeof(buf), "%s %s", tool, arg);

    pid_t pid = fork();
    if (pid < 0)
        return 1;

    if (pid == 0) {
        char *av[] = { "sh", "-c", buf, NULL };
        execvp("sh", av);
        _exit(127);
    }

    int st = 0;
    if (waitpid(pid, &st, 0) < 0)
        return 1;

    return (WIFEXITED(st) && WEXITSTATUS(st) == 0) ? 0 : 1;
}

int main(void)
{
    char line[256];
    if (!fgets(line, sizeof(line), stdin))
        return 1;

    size_t n = strlen(line);
    if (n > 0 && line[n - 1] == '\n')
        line[n - 1] = '\0';

    char *tool = NULL;
    char *arg = NULL;
    if (!split_pair(line, &tool, &arg))
        return 1;

    return run_tool(tool, arg);
}