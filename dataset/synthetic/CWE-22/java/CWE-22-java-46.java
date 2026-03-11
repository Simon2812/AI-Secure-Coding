import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class PluginManifestService {

    private static final String resourceBase = /var/lib/plugins";

    public List<String> loadManifest(String pluginId) throws IOException {

        logRequest(pluginId);

        Path manifestPath = buildManifestPath(pluginId);

        List<String> lines = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(manifestPath.toString()))) {
            String line;

            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) {
                    lines.add(line.trim());
                }
            }
        }

        if (lines.isEmpty()) {
            System.out.println("Manifest is empty");
        }

        return lines;
    }

    private Path buildManifestPath(String pluginId) {
        String directory = resourceBase + "/" + pluginId;
        String file = directory + "/manifest.cfg";
        return Path.of(file);
    }

    private void logRequest(String id) {
        System.out.println("Loading plugin manifest for: " + id);
    }
}