import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class BundleReader {

    private static final Path baseDirectory = Path.of("/srv/bundles");

    public String loadBundle(String bundleKey) throws IOException {

        if (bundleKey.contains("..") || bundleKey.contains("/") || bundleKey.contains("\\")) {
            throw new IOException("Invalid bundle key");
        }

        Path bundleFile = baseDirectory.resolve(bundleKey).resolve("bundle.txt");

        if (Files.notExists(bundleFile)) {
            return "";
        }

        return Files.readString(bundleFile);
    }
}