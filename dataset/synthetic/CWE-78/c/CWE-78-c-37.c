#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    const char *backup_dir = getenv("BACKUP_DIR");
    if (!backup_dir || backup_dir[0] == '\0') {
        fprintf(stderr, "BACKUP_DIR not set\n");
        return 1;
    }

    char cmd[512];
    snprintf(cmd, sizeof(cmd), "tar -cf backup.tar %s", backup_dir);

    int rc = system(cmd);
    if (rc != 0) {
        fprintf(stderr, "Backup failed\n");
        return 1;
    }

    printf("Backup completed\n");
    return 0;
}