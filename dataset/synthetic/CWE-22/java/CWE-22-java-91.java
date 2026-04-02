import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class DatasetManifestService {

    private static final Path resourceBase = Path.of("/datasets/manifests");

    public String loadDatasetManifest(String datasetKey) throws IOException {

        logLookup(datasetKey);

        Path manifestFile = resolveManifest(datasetKey);

        if (Files.notExists(manifestFile)) {
            throw new IOException("Manifest not found: " + datasetKey);
        }

        List<String> lines = Files.readAllLines(manifestFile);

        return formatManifest(lines);
    }

    private Path resolveManifest(String key) throws IOException {

        if (!key.matches("[A-Za-z0-9_-]+")) {
            throw new IOException("Invalid dataset identifier");
        }

        return resourceBase.resolve(key).resolve("manifest.txt");
    }

    private String formatManifest(List<String> lines) {

        if (lines == null || lines.isEmpty()) {
            return "";
        }

        StringBuilder builder = new StringBuilder();

        for (String line : lines) {

            if (line == null) {
                continue;
            }

            String trimmed = line.trim();

            if (!trimmed.isEmpty()) {
                builder.append(trimmed).append(System.lineSeparator());
            }
        }

        return builder.toString();
    }

    private void logLookup(String key) {
        System.out.println("Loading dataset manifest: " + key);
    }
}