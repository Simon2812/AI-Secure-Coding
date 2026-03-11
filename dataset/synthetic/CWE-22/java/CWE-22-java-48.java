import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class TemplateRenderer {

    private static final Path baseDirectory = Path.of("/srv/templates");

    public String renderTemplate(String templateName) throws IOException {

        Path templateFile = locateTemplate(templateName);

        List<String> content = readTemplate(templateFile);

        return mergeContent(content);
    }

    private Path locateTemplate(String name) {
        String filename = name + ".tpl";
        return baseDirectory.resolve(filename);
    }

    private List<String> readTemplate(Path file) throws IOException {

        List<String> lines = new ArrayList<>();

        try (BufferedReader reader = Files.newBufferedReader(file)) {
            String line;

            while ((line = reader.readLine()) != null) {
                lines.add(line);
            }
        }

        return lines;
    }

    private String mergeContent(List<String> lines) {

        StringBuilder builder = new StringBuilder();

        for (String line : lines) {
            builder.append(line).append(System.lineSeparator());
        }

        return builder.toString();
    }
}