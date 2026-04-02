#include <stdio.h>
#include <string.h>

#define MAX_TASKS 64
#define NAME_LEN 32
#define LINE_LEN 128

typedef struct {
    char name[NAME_LEN];
    int interval;
    int enabled;
} TaskConfig;

typedef struct {
    TaskConfig tasks[MAX_TASKS];
    int count;
} SchedulerConfig;

typedef struct {
    int executed;
    int skipped;
} SchedulerStats;

int parse_config_line(const char *line, TaskConfig *task) {
    char name[NAME_LEN];
    int interval;
    int enabled;

    if (sscanf(line, "%31s %d %d", name, &interval, &enabled) != 3) {
        return 0;
    }

    if (interval <= 0) {
        return 0;
    }

    snprintf(task->name, NAME_LEN, "%s", name);
    task->interval = interval;
    task->enabled = enabled ? 1 : 0;

    return 1;
}

int load_config(const char *path, SchedulerConfig *cfg) {
    FILE *fp = fopen(path, "r");
    char line[LINE_LEN];

    if (!fp) {
        return 0;
    }

    cfg->count = 0;

    while (fgets(line, sizeof(line), fp)) {
        TaskConfig t;

        if (cfg->count >= MAX_TASKS) {
            break;
        }

        if (parse_config_line(line, &t)) {
            cfg->tasks[cfg->count++] = t;
        }
    }

    fclose(fp);
    return 1;
}

int should_run(const TaskConfig *task, int current_time) {
    if (!task->enabled) {
        return 0;
    }

    return (current_time % task->interval) == 0;
}

void execute_task(const TaskConfig *task, int current_time) {
    printf("Time %d: Executing task '%s'\n", current_time, task->name);
}

void process_tasks(const SchedulerConfig *cfg,
                   int current_time,
                   SchedulerStats *stats) {

    int i;

    for (i = 0; i < cfg->count; ++i) {
        const TaskConfig *task = &cfg->tasks[i];

        if (should_run(task, current_time)) {
            execute_task(task, current_time);
            stats->executed++;
        } else {
            stats->skipped++;
        }
    }
}

void run_scheduler(const SchedulerConfig *cfg,
                   int start,
                   int end,
                   SchedulerStats *stats) {

    int t;

    for (t = start; t <= end; ++t) {
        process_tasks(cfg, t, stats);
    }
}

void print_stats(const SchedulerStats *stats) {
    printf("\n--- Scheduler Stats ---\n");
    printf("Executed: %d\n", stats->executed);
    printf("Skipped: %d\n", stats->skipped);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <config_file>\n", argv[0]);
        return 1;
    }

    SchedulerConfig config;

    if (!load_config(argv[1], &config)) {
        printf("Failed to load config\n");
        return 1;
    }

    if (config.count == 0) {
        printf("No valid tasks\n");
        return 1;
    }

    SchedulerStats stats;
    stats.executed = 0;
    stats.skipped = 0;

    run_scheduler(&config, 1, 10, &stats);

    print_stats(&stats);

    return 0;
}
