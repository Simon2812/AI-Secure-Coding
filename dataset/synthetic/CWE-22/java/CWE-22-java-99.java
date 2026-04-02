import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

public class ModuleDescriptionService {

    private static final Path ROOT = Path.of("/srv/modules");

    private static final Map<String, String> MODULES = Map.of(
            "alpha", "alpha/description.txt",
            "beta", "beta/description.txt",
            "gamma", "gamma/description.txt"
    );

    public String loadDescription(String moduleKey) throws IOException {

        String relative = MODULES.get(moduleKey);

        if (relative == null) {
            return "";
        }

        Path descriptionFile = ROOT.resolve(relative);

        if (Files.notExists(descriptionFile)) {
            return "";
        }

        List<String> lines = Files.readAllLines(descriptionFile);

        return combine(lines);
    }

    private String combine(List<String> lines) {

        if (lines == null || lines.isEmpty()) {
            return "";
        }

        StringBuilder builder = new StringBuilder();

        for (String line : lines) {

            if (line == null) {
                continue;
            }

            String trimmed = line.trim();

            if (!trimmed.isEmpty()) {
                builder.append(trimmed).append(System.lineSeparator());
            }
        }

        return builder.toString();
    }
}
