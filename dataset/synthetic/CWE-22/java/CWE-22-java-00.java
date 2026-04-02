import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class ActivityLogService {

    private static final Path ROOT = Path.of("/srv/activity/logs");

    public List<String> readEntries(String logName) throws IOException {

        Path logFile = resolveLog(logName);

        if (Files.notExists(logFile)) {
            return new ArrayList<>();
        }

        return collect(logFile);
    }

    private Path resolveLog(String name) throws IOException {

        if (name.contains("..") || name.contains("/") || name.contains("\\")) {
            throw new IOException("Invalid log identifier");
        }

        return ROOT.resolve(name + ".log");
    }

    private List<String> collect(Path file) throws IOException {

        List<String> result = new ArrayList<>();

        try (BufferedReader reader = Files.newBufferedReader(file)) {

            String line;

            while ((line = reader.readLine()) != null) {

                if (line != null && !line.trim().isEmpty()) {
                    result.add(line.trim());
                }
            }
        }

        return result;
    }
}