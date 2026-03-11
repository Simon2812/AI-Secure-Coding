import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class PolicyTemplateService {

    private static final Path ROOT = Path.of("/srv/policies/templates");

    public String loadTemplate(String templateKey) throws IOException {

        logLookup(templateKey);

        Path templateFile = resolveTemplateFile(templateKey);

        if (Files.notExists(templateFile)) {
            throw new IOException("Template not found: " + templateKey);
        }

        String content = Files.readString(templateFile);

        return normalizeTemplate(content);
    }

    private Path resolveTemplateFile(String key) {
        return ROOT.resolve(key).resolve("template.txt");
    }

    private String normalizeTemplate(String text) {

        if (text == null) {
            return "";
        }

        String trimmed = text.trim();

        if (trimmed.isEmpty()) {
            return "";
        }

        return trimmed;
    }

    private void logLookup(String key) {
        System.out.println("Loading policy template: " + key);
    }
}