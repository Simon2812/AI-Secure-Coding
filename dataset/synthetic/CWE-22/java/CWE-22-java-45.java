import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class SnapshotService {

    private static final Path snapshotStore = Path.of("/mnt/archive/snapshots");

    public String loadSnapshot(String snapshotName) throws IOException {

        Path snapshot = snapshotStore.resolve(snapshotName);

        if (Files.notExists(snapshot)) {
            return "";
        }

        return Files.readString(snapshot);
    }
}