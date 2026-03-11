import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ArtifactReader {

    private static final Path ROOT = Path.of("/srv/artifacts");

    public String loadArtifact(String artifactName) throws IOException {

        String safeName = Path.of(artifactName).getFileName().toString();

        Path artifactFile = ROOT.resolve(safeName);

        if (Files.notExists(artifactFile)) {
            return "";
        }

        return Files.readString(artifactFile);
    }
}