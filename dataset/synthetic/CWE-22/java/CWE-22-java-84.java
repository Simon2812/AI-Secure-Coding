import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class SnapshotReader {

    private static final Path dataLocation = Path.of("/srv/snapshots");

    public String readSnapshot(String snapshotKey) throws IOException {

        Path base = dataLocation.toAbsolutePath().normalize();
        Path target = base.resolve(snapshotKey).resolve("snapshot.txt").normalize();

        if (!target.startsWith(base)) {
            throw new IOException("Invalid snapshot path");
        }

        if (Files.notExists(target)) {
            return "";
        }

        return Files.readString(target);
    }
}