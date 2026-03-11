import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class SnapshotArchiveService {

    private static final Path storagePath = Path.of("/datasets/snapshots");

    public List<String> readSnapshot(String snapshotName) throws IOException {

        logAccess(snapshotName);

        Path snapshotFile = resolveSnapshotFile(snapshotName);

        if (Files.notExists(snapshotFile)) {
            throw new IOException("Snapshot not found: " + snapshotName);
        }

        List<String> records = new ArrayList<>();

        try (var lines = Files.lines(snapshotFile)) {

            lines.forEach(line -> {
                if (isValidRecord(line)) {
                    records.add(line.trim());
                }
            });
        }

        return records;
    }

    private Path resolveSnapshotFile(String name) {
        return storagePath.resolve(name);
    }

    private boolean isValidRecord(String line) {

        if (line == null) {
            return false;
        }

        String trimmed = line.trim();

        return !trimmed.isEmpty();
    }

    private void logAccess(String snapshot) {
        System.out.println("Reading snapshot: " + snapshot);
    }
}