import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

public class ProfileTemplateService {

    private static final Path baseDirectory = Path.of("/opt/profile-templates");

    private static final Map<String, String> PROFILES = Map.of(
            "basic", "basic/template.txt",
            "advanced", "advanced/template.txt",
            "compact", "compact/template.txt"
    );

    public String loadTemplate(String profileKey) throws IOException {

        String relative = PROFILES.get(profileKey);

        if (relative == null) {
            return "";
        }

        Path templateFile = baseDirectory.resolve(relative);

        if (Files.notExists(templateFile)) {
            return "";
        }

        List<String> lines = Files.readAllLines(templateFile);

        return merge(lines);
    }

    private String merge(List<String> lines) {

        if (lines == null || lines.isEmpty()) {
            return "";
        }

        StringBuilder result = new StringBuilder();

        for (String line : lines) {

            if (line == null) {
                continue;
            }

            String trimmed = line.trim();

            if (!trimmed.isEmpty()) {
                result.append(trimmed).append(System.lineSeparator());
            }
        }

        return result.toString();
    }
}