import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class BackupConfigManager {

    private static final Path ROOT = Path.of("/srv/backup/configs");

    public Map<String, String> loadConfiguration(String profileName) throws IOException {

        logProfileAccess(profileName);

        Path configFile = resolveConfigFile(profileName);

        if (Files.notExists(configFile)) {
            throw new IOException("Configuration profile not found: " + profileName);
        }

        List<String> lines = Files.readAllLines(configFile);

        return parseConfiguration(lines);
    }

    private Path resolveConfigFile(String profile) {
        return ROOT.resolve(profile).resolve("backup.conf");
    }

    private Map<String, String> parseConfiguration(List<String> lines) {

        Map<String, String> result = new HashMap<>();

        for (String line : lines) {

            if (line == null) {
                continue;
            }

            String trimmed = line.trim();

            if (trimmed.isEmpty()) {
                continue;
            }

            int separator = trimmed.indexOf('=');

            if (separator > 0) {
                String key = trimmed.substring(0, separator).trim();
                String value = trimmed.substring(separator + 1).trim();
                result.put(key, value);
            }
        }

        return result;
    }

    private void logProfileAccess(String name) {
        System.out.println("Loading backup profile: " + name);
    }
}