import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class TemplateStore {

    private static final Path repositoryRoot = Path.of("/data/templates");

    public String loadTemplate(String templateKey) throws IOException {

        if (!templateKey.matches("[A-Za-z0-9_-]+")) {
            throw new IOException("Invalid template key");
        }

        Path file = repositoryRoot.resolve(templateKey + ".tpl");

        if (Files.notExists(file)) {
            return "";
        }

        return Files.readString(file);
    }
}