import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class AnalyticsReportService {

    private static final Path ROOT = Path.of("/opt/appdata/analytics");

    public List<String> collectReportHeaders(String projectKey) throws IOException {

        Path reportDirectory = resolveProjectDirectory(projectKey);

        if (!Files.exists(reportDirectory)) {
            throw new IOException("Project directory not found: " + projectKey);
        }

        List<String> headers = new ArrayList<>();

        try (var paths = Files.list(reportDirectory)) {
            paths.forEach(file -> {
                if (Files.isRegularFile(file)) {
                    try {
                        headers.add(readHeader(file));
                    } catch (IOException e) {
                        System.out.println("Skipping unreadable file: " + file);
                    }
                }
            });
        }

        return headers;
    }

    private Path resolveProjectDirectory(String key) {
        return ROOT.resolve(key);
    }

    private String readHeader(Path file) throws IOException {

        try (var lines = Files.lines(file)) {
            return lines.findFirst().orElse("");
        }
    }
}