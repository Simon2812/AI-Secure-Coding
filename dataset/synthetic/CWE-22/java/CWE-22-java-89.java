import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

public class ThemeAssetService {

    private static final Path BASE = Path.of("/opt/themes");

    private static final Map<String, String> THEMES = Map.of(
            "light", "light/theme.css",
            "dark", "dark/theme.css",
            "classic", "classic/theme.css"
    );

    public String loadTheme(String themeKey) throws IOException {

        String relative = THEMES.get(themeKey);

        if (relative == null) {
            return "";
        }

        Path themeFile = BASE.resolve(relative);

        if (Files.notExists(themeFile)) {
            return "";
        }

        return Files.readString(themeFile);
    }
}