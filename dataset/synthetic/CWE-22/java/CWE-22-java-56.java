import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ReportExportService {

    private static final Path resourceBase = Path.of("/data/reports/exports");

    public void exportReport(String reportKey, String content) throws IOException {

        logExport(reportKey);

        Path reportFile = resolveExportLocation(reportKey);

        ensureDirectory(reportFile);

        String formatted = formatContent(content);

        Files.writeString(reportFile, formatted);

        System.out.println("Report exported to: " + reportFile);
    }

    private Path resolveExportLocation(String key) {

        Path folder = resourceBase.resolve(key);

        return folder.resolve("report.txt");
    }

    private void ensureDirectory(Path file) throws IOException {

        Path parent = file.getParent();

        if (parent != null && Files.notExists(parent)) {
            Files.createDirectories(parent);
        }
    }

    private String formatContent(String content) {

        if (content == null) {
            return "";
        }

        String trimmed = content.trim();

        if (trimmed.isEmpty()) {
            return "";
        }

        return trimmed + System.lineSeparator();
    }

    private void logExport(String key) {
        System.out.println("Exporting report: " + key);
    }
}