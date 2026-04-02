#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define MAX_LINE 256
#define MAX_FIELD 128

typedef struct {
    char tool[MAX_FIELD];
    char arg1[MAX_FIELD];
    char arg2[MAX_FIELD];
} AgentConfig;

typedef struct {
    char target[MAX_FIELD]; /
} ProbeRequest;

static void log_msg(const char *lvl, const char *msg) {
    fprintf(stderr, "[%s] %s\n", lvl, msg);
}

static void trim(char *s) {
    size_t n = strlen(s);
    while (n > 0 && (s[n - 1] == '\n' || s[n - 1] == '\r' || isspace((unsigned char)s[n - 1]))) {
        s[n - 1] = '\0';
        n--;
    }
}

static void set_default_config(AgentConfig *cfg) {
    memset(cfg, 0, sizeof(*cfg));
    strncpy(cfg->tool, "ping", sizeof(cfg->tool) - 1);
    strncpy(cfg->arg1, "-c", sizeof(cfg->arg1) - 1);
    strncpy(cfg->arg2, "1", sizeof(cfg->arg2) - 1);
}

static int load_config(const char *path, AgentConfig *cfg) {
    FILE *f = fopen(path, "r");
    if (!f) {
        log_msg("WARN", "config not found; using defaults");
        set_default_config(cfg);
        return 0;
    }

    set_default_config(cfg);

    char line[MAX_LINE];
    while (fgets(line, sizeof(line), f)) {
        trim(line);
        if (line[0] == '\0' || line[0] == '#') continue;

        char *eq = strchr(line, '=');
        if (!eq) continue;

        *eq = '\0';
        const char *k = line;
        const char *v = eq + 1;

        if (strcmp(k, "tool") == 0) {
            strncpy(cfg->tool, v, sizeof(cfg->tool) - 1);
        } else if (strcmp(k, "arg1") == 0) {
            strncpy(cfg->arg1, v, sizeof(cfg->arg1) - 1);
        } else if (strcmp(k, "arg2") == 0) {
            strncpy(cfg->arg2, v, sizeof(cfg->arg2) - 1);
        }
    }

    fclose(f);
    return 0;
}

static int parse_request(const char *line, ProbeRequest *req) {
    memset(req, 0, sizeof(*req));

    if (strncmp(line, "probe ", 6) != 0) return -1;

    const char *t = line + 6;
    while (*t == ' ') t++;

    if (*t == '\0') return -1;

    strncpy(req->target, t, sizeof(req->target) - 1);
    trim(req->target);
    return 0;
}

static int run_probe_vulnerable(const AgentConfig *cfg, const ProbeRequest *req) {
    char cmd[512];

    snprintf(cmd, sizeof(cmd), "%s %s %s %s", cfg->tool, cfg->arg1, cfg->arg2, req->target);

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        return -1;
    }
    if (pid == 0) {
        execl("/bin/sh", "sh", "-c", cmd, (char *)NULL);
        perror("execl");
        _exit(127);
    }

    int status = 0;
    if (waitpid(pid, &status, 0) < 0) {
        perror("waitpid");
        return -1;
    }
    if (!WIFEXITED(status) || WEXITSTATUS(status) != 0) {
        log_msg("ERROR", "probe command failed");
        return -1;
    }
    return 0;
}

static void print_help(void) {
    puts("Commands:");
    puts("  probe <host-or-ip>   run a quick connectivity probe");
    puts("  reload              reload agent.conf");
    puts("  quit                exit");
}

int main(void) {
    AgentConfig cfg;
    load_config("agent.conf", &cfg);

    log_msg("INFO", "agent started");
    print_help();

    char line[MAX_LINE];
    while (1) {
        fputs("> ", stdout);
        if (!fgets(line, sizeof(line), stdin)) break;
        trim(line);

        if (line[0] == '\0') continue;

        if (strcmp(line, "quit") == 0) {
            log_msg("INFO", "shutting down");
            break;
        }

        if (strcmp(line, "reload") == 0) {
            load_config("agent.conf", &cfg);
            log_msg("INFO", "config reloaded");
            continue;
        }

        if (strcmp(line, "help") == 0) {
            print_help();
            continue;
        }

        ProbeRequest req;
        if (parse_request(line, &req) == 0) {
            if (run_probe_vulnerable(&cfg, &req) == 0) {
                log_msg("INFO", "probe ok");
            }
            continue;
        }

        log_msg("WARN", "unknown command; type 'help'");
    }

    return 0;
}