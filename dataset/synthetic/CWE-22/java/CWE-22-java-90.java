import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class LogEntryReader {

    private static final Path baseDirectory = Path.of("/var/logs");

    public String readLog(String logName) throws IOException {

        String sanitized = sanitize(logName);

        Path logFile = baseDirectory.resolve(sanitized + ".log");

        if (Files.notExists(logFile)) {
            return "";
        }

        return Files.readString(logFile);
    }

    private String sanitize(String name) {

        if (name == null) {
            return "default";
        }

        String cleaned = name.replace("..", "");
        cleaned = cleaned.replace("/", "");
        cleaned = cleaned.replace("\\", "");

        if (cleaned.isEmpty()) {
            return "default";
        }

        return cleaned;
    }
}