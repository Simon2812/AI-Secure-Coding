import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ThumbnailCacheService {

    private static final Path ROOT = Path.of("/srv/cache/thumbnails");

    public String loadThumbnailMetadata(String imageId) throws IOException {

        logLookup(imageId);

        Path metadataFile = resolveMetadataFile(imageId);

        if (Files.notExists(metadataFile)) {
            System.out.println("Metadata missing for image: " + imageId);
            return "";
        }

        String metadata = Files.readString(metadataFile);

        return normalizeMetadata(metadata);
    }

    private Path resolveMetadataFile(String id) {
        return ROOT.resolve(id + ".meta");
    }

    private String normalizeMetadata(String metadata) {

        if (metadata == null) {
            return "";
        }

        String trimmed = metadata.trim();

        if (trimmed.isEmpty()) {
            return "";
        }

        return trimmed;
    }

    private void logLookup(String key) {
        System.out.println("Loading thumbnail metadata for: " + key);
    }
}