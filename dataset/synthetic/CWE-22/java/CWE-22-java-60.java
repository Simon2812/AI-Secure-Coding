import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class DatasetReportService {

    private static final Path storagePath = Path.of("/srv/dataset-reports");

    public List<String> readReport(String reportName) throws IOException {

        logAccess(reportName);

        Path reportFile = resolveReportFile(reportName);

        if (Files.notExists(reportFile)) {
            throw new IOException("Report not found: " + reportName);
        }

        List<String> entries = new ArrayList<>();

        try (BufferedReader reader = Files.newBufferedReader(reportFile)) {

            String line;

            while ((line = reader.readLine()) != null) {
                if (isRelevant(line)) {
                    entries.add(line.trim());
                }
            }
        }

        return entries;
    }

    private Path resolveReportFile(String name) {
        return storagePath.resolve(name + ".report");
    }

    private boolean isRelevant(String line) {

        if (line == null) {
            return false;
        }

        String trimmed = line.trim();

        return !trimmed.isEmpty();
    }

    private void logAccess(String name) {
        System.out.println("Reading dataset report: " + name);
    }
}