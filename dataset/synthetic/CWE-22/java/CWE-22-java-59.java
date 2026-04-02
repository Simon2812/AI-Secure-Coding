import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class ConfigBundleService {

    private static final Path ROOT = Path.of("/opt/config-bundles");

    public List<String> loadBundleKeys(String bundleName) throws IOException {

        logBundleAccess(bundleName);

        Path bundleDirectory = resolveBundleDirectory(bundleName);

        if (Files.notExists(bundleDirectory)) {
            throw new IOException("Bundle not found: " + bundleName);
        }

        List<String> keys = new ArrayList<>();

        try (var paths = Files.walk(bundleDirectory)) {

            paths.filter(Files::isRegularFile)
                 .forEach(file -> {
                     try {
                         keys.add(readKey(file));
                     } catch (IOException e) {
                         System.out.println("Skipping unreadable config: " + file);
                     }
                 });
        }

        return keys;
    }

    private Path resolveBundleDirectory(String name) {
        return ROOT.resolve(name);
    }

    private String readKey(Path file) throws IOException {

        List<String> lines = Files.readAllLines(file);

        if (lines.isEmpty()) {
            return "";
        }

        return lines.get(0).trim();
    }

    private void logBundleAccess(String bundle) {
        System.out.println("Loading configuration bundle: " + bundle);
    }
}