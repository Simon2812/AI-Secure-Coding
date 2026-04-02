import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class SnapshotEntryService {

    private static final Path BASE = Path.of("/storage/snapshots");

    public List<String> readEntries(String snapshotName) throws IOException {

        Path snapshotFile = locateSnapshot(snapshotName);

        if (Files.notExists(snapshotFile)) {
            return new ArrayList<>();
        }

        return collectEntries(snapshotFile);
    }

    private Path locateSnapshot(String name) {

        String filename = Path.of(name).getFileName().toString();

        return BASE.resolve(filename + ".snapshot");
    }

    private List<String> collectEntries(Path file) throws IOException {

        List<String> entries = new ArrayList<>();

        try (BufferedReader reader = Files.newBufferedReader(file)) {

            String line;

            while ((line = reader.readLine()) != null) {

                if (line != null && !line.trim().isEmpty()) {
                    entries.add(line.trim());
                }
            }
        }

        return entries;
    }
}