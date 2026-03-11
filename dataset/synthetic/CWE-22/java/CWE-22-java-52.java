import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class SystemLogService {

    private static final Path BASE = Path.of("/var/systemlogs");

    public List<String> readLog(String logFile) throws IOException {

        logRequest(logFile);

        Path file = resolveLogFile(logFile);

        if (Files.notExists(file)) {
            throw new IOException("Log file not found: " + logFile);
        }

        List<String> entries = new ArrayList<>();

        try (BufferedReader reader = Files.newBufferedReader(file)) {

            String line;

            while ((line = reader.readLine()) != null) {

                if (isRelevant(line)) {
                    entries.add(line);
                }
            }
        }

        return entries;
    }

    private Path resolveLogFile(String name) {
        return BASE.resolve(name);
    }

    private boolean isRelevant(String line) {

        if (line == null) {
            return false;
        }

        String trimmed = line.trim();

        return !trimmed.isEmpty();
    }

    private void logRequest(String file) {
        System.out.println("Reading log file: " + file);
    }
}