import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class ArtifactStorageService {

    private static final Path dataLocation = Path.of("/srv/artifacts");

    public void storeArtifact(String artifactName, String data) throws IOException {

        logStore(artifactName);

        Path artifactFile = resolveArtifactFile(artifactName);

        ensureDirectory(artifactFile);

        byte[] payload = preparePayload(data);

        try (OutputStream out = Files.newOutputStream(
                artifactFile,
                StandardOpenOption.CREATE,
                StandardOpenOption.TRUNCATE_EXISTING,
                StandardOpenOption.WRITE)) {

            out.write(payload);
        }

        System.out.println("Artifact stored at: " + artifactFile);
    }

    private Path resolveArtifactFile(String name) {
        return dataLocation.resolve(name);
    }

    private void ensureDirectory(Path file) throws IOException {

        Path parent = file.getParent();

        if (parent != null && Files.notExists(parent)) {
            Files.createDirectories(parent);
        }
    }

    private byte[] preparePayload(String data) {

        if (data == null) {
            return new byte[0];
        }

        String normalized = data.trim();

        if (normalized.isEmpty()) {
            return new byte[0];
        }

        normalized = normalized + System.lineSeparator();

        return normalized.getBytes(StandardCharsets.UTF_8);
    }

    private void logStore(String name) {
        System.out.println("Storing artifact: " + name);
    }
}