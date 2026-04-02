import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ResourceFetcher {

    private static final Path repository = Path.of("/opt/appdata/resources");

    public String loadResource(String resource) throws IOException {

        Path path = Path.of(repository.toString(), resource);

        if (Files.notExists(path)) {
            return "";
        }

        return Files.readString(path);
    }
}