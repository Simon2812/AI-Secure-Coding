import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class ConfigurationRegistry {

    private static final Path ROOT = Path.of("/data/storage/configs");

    public List<String> loadConfiguration(String configName) throws IOException {

        logLookup(configName);

        Path configFile = resolveConfigPath(configName);

        if (!Files.exists(configFile)) {
            throw new IOException("Configuration not found: " + configName);
        }

        List<String> lines = Files.readAllLines(configFile);

        if (lines.isEmpty()) {
            System.out.println("Configuration file is empty");
        }

        return lines;
    }

    private Path resolveConfigPath(String name) {
        Path dir = ROOT.resolve(name);
        return dir.resolve("settings.conf");
    }

    private void logLookup(String key) {
        System.out.println("Loading configuration: " + key);
    }
}