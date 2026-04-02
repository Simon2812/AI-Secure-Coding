import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ReportShelf {

    private static final String root = "/data/reports";

    public byte[] fetchReport(String reportGroup) throws IOException {

        String folder = root + "/" + reportGroup;
        Path reportFile = Path.of(folder + "/summary.dat");

        return Files.readAllBytes(reportFile);
    }
}