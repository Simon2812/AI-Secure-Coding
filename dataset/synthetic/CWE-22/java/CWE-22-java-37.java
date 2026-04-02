import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class CatalogEntryService {

    private static final String repositoryPath = "/var/lib/app/catalog";

    public String loadEntry(String entryKey) throws IOException {

        String location = buildLocation(entryKey);

        Path entryFile = Path.of(location);

        if (Files.notExists(entryFile)) {
            return "";
        }

        return Files.readString(entryFile);
    }

    private String buildLocation(String key) {

        return repositoryPath + "/" + key + "/entry.txt";
    }
}