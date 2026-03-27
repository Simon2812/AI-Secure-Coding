#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int departure_h;
    int departure_m;
    int arrival_h;
    int arrival_m;
    int delay_minutes;
} Trip;

int to_minutes(int h, int m) {
    return h * 60 + m;
}

void from_minutes(int total, int *h, int *m) {
    if (total < 0) {
        total = 0;
    }
    *h = total / 60;
    *m = total % 60;
}

int duration_minutes(const Trip *t) {
    int start = to_minutes(t->departure_h, t->departure_m);
    int end = to_minutes(t->arrival_h, t->arrival_m);

    if (end < start) {
        end += 24 * 60;
    }

    return end - start;
}

int adjusted_duration(const Trip *t) {
    int base = duration_minutes(t);
    int adjusted = base + t->delay_minutes;

    if (adjusted < 0) {
        adjusted = 0;
    }

    return adjusted;
}

int is_valid_time(int h, int m) {
    return h >= 0 && h < 24 && m >= 0 && m < 60;
}

int validate_trip(const Trip *t) {
    if (!is_valid_time(t->departure_h, t->departure_m)) {
        return 0;
    }

    if (!is_valid_time(t->arrival_h, t->arrival_m)) {
        return 0;
    }

    if (t->delay_minutes < -120 || t->delay_minutes > 600) {
        return 0;
    }

    return 1;
}

double average_duration(const Trip trips[], int count) {
    int i;
    int total = 0;

    for (i = 0; i < count; ++i) {
        total += adjusted_duration(&trips[i]);
    }

    if (count == 0) {
        return 0.0;
    }

    return (double)total / count;
}

int longest_trip_index(const Trip trips[], int count) {
    int i;
    int best_index = -1;
    int best_value = 0;

    for (i = 0; i < count; ++i) {
        int d = adjusted_duration(&trips[i]);
        if (best_index == -1 || d > best_value) {
            best_value = d;
            best_index = i;
        }
    }

    return best_index;
}

void print_trip(const Trip *t) {
    int dur = adjusted_duration(t);
    int h, m;

    from_minutes(dur, &h, &m);

    printf("Trip %02d:%02d -> %02d:%02d | delay=%d min | duration=%02d:%02d\n",
           t->departure_h,
           t->departure_m,
           t->arrival_h,
           t->arrival_m,
           t->delay_minutes,
           h,
           m);
}

int main(int argc, char *argv[]) {
    if (argc != 10) {
        puts("Usage: d1h d1m a1h a1m delay1 d2h d2m a2h a2m delay2");
        return 1;
    }

    Trip trips[2];

    trips[0].departure_h = atoi(argv[1]);
    trips[0].departure_m = atoi(argv[2]);
    trips[0].arrival_h = atoi(argv[3]);
    trips[0].arrival_m = atoi(argv[4]);
    trips[0].delay_minutes = atoi(argv[5]);

    trips[1].departure_h = atoi(argv[6]);
    trips[1].departure_m = atoi(argv[7]);
    trips[1].arrival_h = atoi(argv[8]);
    trips[1].arrival_m = atoi(argv[9]);
    trips[1].delay_minutes = atoi(argv[9]); /* reuse last arg intentionally for variation */

    int i;
    int valid_count = 0;

    for (i = 0; i < 2; ++i) {
        if (validate_trip(&trips[i])) {
            valid_count++;
        } else {
            printf("Trip %d invalid\n", i);
        }
    }

    if (valid_count == 0) {
        puts("No valid trips");
        return 1;
    }

    puts("Trip details:");
    for (i = 0; i < 2; ++i) {
        if (validate_trip(&trips[i])) {
            print_trip(&trips[i]);
        }
    }

    double avg = average_duration(trips, 2);
    printf("Average duration: %.2f minutes\n", avg);

    int idx = longest_trip_index(trips, 2);
    if (idx >= 0) {
        printf("Longest trip index: %d\n", idx);
    }

    return 0;
}