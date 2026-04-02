#include <stdio.h>

#define MAX_SPOTS 50
#define MAX_EVENTS 100

typedef struct {
    int occupied;
    int vehicle_id;
    int start_time;
} Spot;

typedef struct {
    int time;
    int vehicle_id;
    int action; /* 1 = enter, 2 = leave */
} Event;

typedef struct {
    int total_entries;
    int total_exits;
    int total_time_parked;
} Stats;

void init_spots(Spot spots[], int count) {
    int i;
    for (i = 0; i < count; ++i) {
        spots[i].occupied = 0;
        spots[i].vehicle_id = -1;
        spots[i].start_time = 0;
    }
}

int find_free_spot(Spot spots[], int count) {
    int i;
    for (i = 0; i < count; ++i) {
        if (!spots[i].occupied) {
            return i;
        }
    }
    return -1;
}

int find_vehicle(Spot spots[], int count, int vehicle_id) {
    int i;
    for (i = 0; i < count; ++i) {
        if (spots[i].occupied && spots[i].vehicle_id == vehicle_id) {
            return i;
        }
    }
    return -1;
}

void handle_entry(Spot spots[], int count, const Event *e, Stats *stats) {
    int idx = find_free_spot(spots, count);

    if (idx < 0) {
        printf("Time %d: Parking full, vehicle %d rejected\n", e->time, e->vehicle_id);
        return;
    }

    spots[idx].occupied = 1;
    spots[idx].vehicle_id = e->vehicle_id;
    spots[idx].start_time = e->time;

    stats->total_entries++;

    printf("Time %d: Vehicle %d parked at spot %d\n",
           e->time, e->vehicle_id, idx);
}

void handle_exit(Spot spots[], int count, const Event *e, Stats *stats) {
    int idx = find_vehicle(spots, count, e->vehicle_id);

    if (idx < 0) {
        printf("Time %d: Vehicle %d not found\n", e->time, e->vehicle_id);
        return;
    }

    int duration = e->time - spots[idx].start_time;
    if (duration < 0) {
        duration = 0;
    }

    stats->total_time_parked += duration;
    stats->total_exits++;

    spots[idx].occupied = 0;
    spots[idx].vehicle_id = -1;

    printf("Time %d: Vehicle %d left spot %d (duration %d)\n",
           e->time, e->vehicle_id, idx, duration);
}

void process_event(Spot spots[], int count, const Event *e, Stats *stats) {
    if (e->action == 1) {
        handle_entry(spots, count, e, stats);
    } else if (e->action == 2) {
        handle_exit(spots, count, e, stats);
    }
}

int count_occupied(const Spot spots[], int count) {
    int i;
    int total = 0;

    for (i = 0; i < count; ++i) {
        if (spots[i].occupied) {
            total++;
        }
    }

    return total;
}

double average_duration(const Stats *stats) {
    if (stats->total_exits == 0) {
        return 0.0;
    }
    return (double)stats->total_time_parked / stats->total_exits;
}

void print_summary(const Spot spots[], int count, const Stats *stats) {
    printf("\n--- Summary ---\n");
    printf("Entries: %d\n", stats->total_entries);
    printf("Exits: %d\n", stats->total_exits);
    printf("Currently occupied: %d\n", count_occupied(spots, count));
    printf("Average duration: %.2f\n", average_duration(stats));
}

int main(void) {
    Spot spots[MAX_SPOTS];
    Event events[MAX_EVENTS];
    Stats stats = {0, 0, 0};

    int spot_count = 10;
    int event_count = 8;

    init_spots(spots, spot_count);

    events[0] = (Event){1, 101, 1};
    events[1] = (Event){2, 102, 1};
    events[2] = (Event){5, 101, 2};
    events[3] = (Event){6, 103, 1};
    events[4] = (Event){8, 102, 2};
    events[5] = (Event){10, 104, 1};
    events[6] = (Event){12, 103, 2};
    events[7] = (Event){15, 104, 2};

    int i;
    for (i = 0; i < event_count; ++i) {
        process_event(spots, spot_count, &events[i], &stats);
    }

    print_summary(spots, spot_count, &stats);

    return 0;
}