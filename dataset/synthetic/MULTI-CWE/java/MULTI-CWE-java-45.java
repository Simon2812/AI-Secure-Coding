import java.io.ByteArrayInputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.nio.charset.StandardCharsets;
import java.util.Properties;
import java.util.Locale;
import java.nio.file.Path;
import java.nio.file.Paths;

public class ProfileInterpreter {

    private final Path root;

    public ProfileInterpreter(String root) {
        this.root = Paths.get(root);
    }

    public View interpret(String rawConfig) throws Exception {

        Properties p = new Properties();
        try (BufferedReader r = new BufferedReader(
                new InputStreamReader(
                        new ByteArrayInputStream(
                                (rawConfig == null ? "" : rawConfig).getBytes(StandardCharsets.UTF_8)
                        ),
                        StandardCharsets.UTF_8))) {
            p.load(r);
        }

        String name = normalize(p.getProperty("name"));
        Path file = chooseFile(p.getProperty("file"));

        return new View(name, file.toString());
    }

    private String normalize(String value) {
        if (value == null) {
            return "default";
        }

        String v = value.trim().toLowerCase(Locale.ROOT);
        return v.matches("[a-z0-9_]+") ? v : "default";
    }

    private Path chooseFile(String raw) {
        String safe = (raw != null && raw.matches("[a-zA-Z0-9._-]+")) ? raw : "profile.cfg";
        return root.resolve(safe).normalize();
    }

    public record View(String name, String filePath) {}
}