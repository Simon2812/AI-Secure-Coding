import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class ConfigurationBundleReader {

    private static final Path resourceBase = Path.of("/srv/configuration/bundles");

    public List<String> loadBundle(String bundleKey) throws IOException {

        Path bundleDirectory = resolveBundle(bundleKey);

        if (Files.notExists(bundleDirectory)) {
            return new ArrayList<>();
        }

        Path configFile = bundleDirectory.resolve("config.txt");

        if (Files.notExists(configFile)) {
            return new ArrayList<>();
        }

        return readLines(configFile);
    }

    private Path resolveBundle(String key) throws IOException {

        if (key.contains("..") || key.contains("/") || key.contains("\\")) {
            throw new IOException("Invalid bundle identifier");
        }

        return resourceBase.resolve(key);
    }

    private List<String> readLines(Path file) throws IOException {

        List<String> result = new ArrayList<>();

        try (BufferedReader reader = Files.newBufferedReader(file)) {

            String line;

            while ((line = reader.readLine()) != null) {

                if (line != null && !line.trim().isEmpty()) {
                    result.add(line.trim());
                }
            }
        }

        return result;
    }
}