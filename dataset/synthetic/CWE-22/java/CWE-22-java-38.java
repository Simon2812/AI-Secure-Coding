import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ProfileConfigService {

    private static final Path dataRoot = Path.of("/opt/appdata/profiles");

    public String readProfile(String profileName) throws IOException {

        Path profileFile = resolveProfile(profileName);

        if (Files.notExists(profileFile)) {
            return "";
        }

        return Files.readString(profileFile);
    }

    private Path resolveProfile(String name) {
        return dataRoot.resolve(name + ".conf");
    }
}