import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class AnalyticsReportService {

    private static final Path catalogRoot = Path.of("/data/storage/reports");

    public String readReportHeader(String reportKey) throws IOException {

        Path reportFile = locateReport(reportKey);

        if (Files.notExists(reportFile)) {
            return "";
        }

        List<String> lines = Files.readAllLines(reportFile);

        if (lines.isEmpty()) {
            return "";
        }

        return lines.get(0);
    }

    private Path locateReport(String key) {
        return catalogRoot.resolve(key).resolve("report.txt");
    }
}