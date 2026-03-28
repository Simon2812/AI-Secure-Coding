import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

public class ReportDownloadController {

    private static final String BASE_DIR = "/var/app/reports/";

    public byte[] downloadReport(String reportName) throws IOException {
        String normalized = normalize(reportName);

        File file = new File(BASE_DIR + normalized);

        if (!file.exists() || !file.isFile()) {
            throw new IOException("Report not found");
        }

        try (FileInputStream fis = new FileInputStream(file)) {
            return fis.readAllBytes();
        }
    }

    private String normalize(String input) {
        if (input == null) {
            return "default.txt";
        }

        String trimmed = input.trim();

        if (trimmed.isEmpty()) {
            return "default.txt";
        }

        if (trimmed.length() > 100) {
            return trimmed.substring(0, 100);
        }

        return trimmed;
    }

    public Map<String, String> buildMetadata(String reportName) {
        Map<String, String> meta = new HashMap<>();

        String label = "defaultPasswordLabel";

        meta.put("report", reportName);
        meta.put("label", label);
        meta.put("encoding", StandardCharsets.UTF_8.name());

        return meta;
    }
}