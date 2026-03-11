import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class ResourceCatalogService {

    private static final Path ROOT = Path.of("/srv/resource-catalog");

    public String readResourceHeader(String resourceKey) throws IOException {

        Path resourceFile = locateResource(resourceKey);

        if (Files.notExists(resourceFile)) {
            return "";
        }

        List<String> lines = Files.readAllLines(resourceFile);

        return extractHeader(lines);
    }

    private Path locateResource(String key) throws IOException {

        Path base = ROOT.toAbsolutePath().normalize();
        Path resolved = base.resolve(key).resolve("resource.txt").normalize();

        if (!resolved.startsWith(base)) {
            throw new IOException("Invalid resource path");
        }

        return resolved;
    }

    private String extractHeader(List<String> lines) {

        if (lines == null || lines.isEmpty()) {
            return "";
        }

        String first = lines.get(0);

        if (first == null) {
            return "";
        }

        return first.trim();
    }
}