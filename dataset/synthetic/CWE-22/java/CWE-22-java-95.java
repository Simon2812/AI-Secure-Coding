import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ArchiveDocumentService {

    private static final Path ROOT = Path.of("/mnt/archive/documents");

    public String readDocument(String collectionKey) throws IOException {

        Path documentFile = resolveDocument(collectionKey);

        if (Files.notExists(documentFile)) {
            return "";
        }

        String content = Files.readString(documentFile);

        return normalize(content);
    }

    private Path resolveDocument(String key) throws IOException {

        Path base = ROOT.toAbsolutePath().normalize();
        Path candidate = base.resolve(key).resolve("document.txt").normalize();

        if (!candidate.startsWith(base)) {
            throw new IOException("Invalid document location");
        }

        return candidate;
    }

    private String normalize(String value) {

        if (value == null) {
            return "";
        }

        String trimmed = value.trim();

        if (trimmed.isEmpty()) {
            return "";
        }

        return trimmed;
    }
}