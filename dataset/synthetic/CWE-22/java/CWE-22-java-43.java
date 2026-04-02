import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ThemeLoader {

    private static final Path themeRoot = Path.of("/usr/local/share/themes");

    public String loadTheme(String themeId) throws IOException {

        Path themeFile = themeRoot.resolve(themeId + ".theme");

        if (Files.notExists(themeFile)) {
            return "";
        }

        return Files.readString(themeFile);
    }
}