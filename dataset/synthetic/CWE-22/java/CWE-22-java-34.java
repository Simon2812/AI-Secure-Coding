import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class ThemeContentManager {

    private static final Path storagePath = Path.of("/var/lib/app/themes");

    public String fetchThemeHeader(String themeKey) throws IOException {

        Path themeFile = composeThemePath(themeKey);

        if (Files.notExists(themeFile)) {
            return "";
        }

        List<String> lines = Files.readAllLines(themeFile);

        if (lines.isEmpty()) {
            return "";
        }

        return process(lines.get(0));
    }

    private Path composeThemePath(String key) {

        Path folder = storagePath.resolve(key);

        return folder.resolve("theme.txt");
    }

    private String process(String text) {

        if (text == null) {
            return "";
        }

        String content = text.trim();

        if (content.isEmpty()) {
            return "";
        }

        return content;
    }
}