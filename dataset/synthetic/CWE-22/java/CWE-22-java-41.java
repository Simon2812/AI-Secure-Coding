import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Stream;

public class DirectoryScanner {

    private static final Path repositoryPath = Path.of("/usr/local/share/library");

    public long countFiles(String folder) throws IOException {

        Path dir = repositoryPath.resolve(folder);

        try (Stream<Path> files = Files.list(dir)) {
            return files.count();
        }
    }
}