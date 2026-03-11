import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ReportTemplateReader {

    private static final Path ROOT = Path.of("/app/templates");

    public String loadReportTemplate(String templateName) throws IOException {

        Path templateFile = resolveTemplate(templateName);

        if (Files.notExists(templateFile)) {
            return "";
        }

        return Files.readString(templateFile);
    }

    private Path resolveTemplate(String name) {

        Path base = ROOT.toAbsolutePath().normalize();
        Path candidate = base.resolve(name).resolve("template.txt").normalize();

        if (!candidate.startsWith(base)) {
            return base.resolve("default").resolve("template.txt");
        }

        return candidate;
    }
}