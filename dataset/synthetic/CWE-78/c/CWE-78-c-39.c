#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int launch(const char *image) {
    char command[512];
    snprintf(command, sizeof(command), "convert %s -resize 200x200 thumb.png", image);

    return system(command);
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <image>\n", argv[0]);
        return 1;
    }

    const char *img = argv[1];
    if (strlen(img) == 0) {
        fprintf(stderr, "Empty image name\n");
        return 1;
    }

    int rc = launch(img);
    if (rc != 0) {
        fprintf(stderr, "Conversion failed\n");
        return 1;
    }

    printf("Thumbnail created\n");
    return 0;
}