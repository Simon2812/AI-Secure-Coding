import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class ConfigProfileReader {

    private static final Path ROOT = Path.of("/srv/configs");

    public List<String> loadProfile(String profileId) throws IOException {

        String safeId = Path.of(profileId).getFileName().toString();

        Path file = ROOT.resolve(safeId + ".conf");

        if (Files.notExists(file)) {
            throw new IOException("Profile not found: " + safeId);
        }

        return Files.readAllLines(file);
    }
}