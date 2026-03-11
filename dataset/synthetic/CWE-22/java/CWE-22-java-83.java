import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ReportRepository {

    private static final Path ROOT = Path.of("/data/storage/reports");

    public String loadReport(String reportId) throws IOException {

        if (reportId.contains("..") || reportId.contains("/") || reportId.contains("\\")) {
            throw new IOException("Invalid report identifier");
        }

        Path reportFile = ROOT.resolve(reportId).resolve("report.txt");

        if (Files.notExists(reportFile)) {
            return "";
        }

        return Files.readString(reportFile);
    }
}