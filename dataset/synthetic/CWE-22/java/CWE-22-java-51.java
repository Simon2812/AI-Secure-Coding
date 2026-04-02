import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class DocumentArchiveService {

    private static final Path ROOT = Path.of("/srv/documents");

    public List<String> collectSummaries(String archiveKey) throws IOException {

        logAccess(archiveKey);

        Path archiveDir = resolveArchiveDirectory(archiveKey);

        if (Files.notExists(archiveDir)) {
            throw new IOException("Archive not found: " + archiveKey);
        }

        List<String> summaries = new ArrayList<>();

        try (var paths = Files.walk(archiveDir)) {

            paths.filter(Files::isRegularFile)
                 .forEach(file -> {
                     try {
                         summaries.add(extractSummary(file));
                     } catch (IOException e) {
                         System.out.println("Skipping unreadable document: " + file);
                     }
                 });
        }

        return summaries;
    }

    private Path resolveArchiveDirectory(String key) {
        return ROOT.resolve(key);
    }

    private String extractSummary(Path file) throws IOException {

        String content = Files.readString(file);

        if (content.length() > 120) {
            return content.substring(0, 120);
        }

        return content;
    }

    private void logAccess(String key) {
        System.out.println("Reading archive: " + key);
    }
}