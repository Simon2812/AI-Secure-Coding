#include <stdio.h>
#include <string.h>

int main(void) {
    int state = 0;  // 0 = stopped, 1 = running, 2 = paused
    char input[64];

    while (1) {
        printf("Enter command (start/stop/pause/resume/exit): ");

        if (!fgets(input, sizeof(input), stdin)) {
            break;
        }

        size_t len = strlen(input);
        if (len > 0 && input[len - 1] == '\n') {
            input[len - 1] = '\0';
        }

        if (strcmp(input, "start") == 0) {
            if (state == 0) {
                state = 1;
                puts("System started");
            } else {
                puts("Already active");
            }
        } else if (strcmp(input, "stop") == 0) {
            if (state != 0) {
                state = 0;
                puts("System stopped");
            } else {
                puts("Already stopped");
            }
        } else if (strcmp(input, "pause") == 0) {
            if (state == 1) {
                state = 2;
                puts("Paused");
            } else {
                puts("Cannot pause");
            }
        } else if (strcmp(input, "resume") == 0) {
            if (state == 2) {
                state = 1;
                puts("Resumed");
            } else {
                puts("Cannot resume");
            }
        } else if (strcmp(input, "exit") == 0) {
            break;
        } else {
            puts("Unknown command");
        }
    }

    return 0;
}