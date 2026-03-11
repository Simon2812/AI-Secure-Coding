import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;

public class SnapshotStore {

    private static final Path ROOT = Path.of("/var/snapshots");

    public int readSnapshot(String snapshotKey) throws IOException {

        Path snapshotFile = resolveSnapshot(snapshotKey);

        InputStream in = Files.newInputStream(snapshotFile);
        return in.read();
    }

    private Path resolveSnapshot(String key) {
        return ROOT.resolve(key).resolve("state.bin");
    }
}