import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class TemplateCatalogService {

    private static final Path ROOT = Path.of("/srv/catalog/templates");

    public String loadTemplate(String templateName) throws IOException {

        logLookup(templateName);

        Path templateFile = resolveTemplate(templateName);

        if (Files.notExists(templateFile)) {
            return "";
        }

        String content = Files.readString(templateFile);

        return normalize(content);
    }

    private Path resolveTemplate(String name) {

        String safeName = Path.of(name).getFileName().toString();

        return ROOT.resolve(safeName + ".tpl");
    }

    private String normalize(String text) {

        if (text == null) {
            return "";
        }

        String trimmed = text.trim();

        if (trimmed.isEmpty()) {
            return "";
        }

        return trimmed + System.lineSeparator();
    }

    private void logLookup(String key) {
        System.out.println("Reading template: " + key);
    }
}