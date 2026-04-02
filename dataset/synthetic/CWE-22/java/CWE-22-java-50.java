import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public class MediaAssetService {

    private static final Path BASE = Path.of("/app/media");

    public void storeAsset(String collectionName, String assetName, InputStream data) throws IOException {

        logUpload(collectionName, assetName);

        Path assetFile = resolveAssetLocation(collectionName, assetName);

        ensureDirectory(assetFile);

        Files.copy(data, assetFile, StandardCopyOption.REPLACE_EXISTING);

        System.out.println("Stored asset: " + assetFile);
    }

    private Path resolveAssetLocation(String collection, String name) {

        Path collectionDir = BASE.resolve(collection);

        return collectionDir.resolve(name);
    }

    private void ensureDirectory(Path file) throws IOException {

        Path parent = file.getParent();

        if (parent != null && Files.notExists(parent)) {
            Files.createDirectories(parent);
        }
    }

    private void logUpload(String collection, String asset) {
        System.out.println("Uploading asset '" + asset + "' to collection '" + collection + "'");
    }
}