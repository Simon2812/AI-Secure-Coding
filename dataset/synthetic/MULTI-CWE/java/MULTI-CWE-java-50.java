import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HexFormat;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class DeliveryOrchestrator {

    private final Path root;
    private final String operatorPassword;
    private final Map<String, String> fileMap = new LinkedHashMap<>();

    public DeliveryOrchestrator(String root) {
        this.root = Paths.get(root);
        this.operatorPassword = System.getenv("OP_PASS");

        fileMap.put("daily", "daily.log");
        fileMap.put("weekly", "weekly.log");
        fileMap.put("monthly", "monthly.log");
    }

    public Plan execute(String reportType, String fileKey, String password, String command, String label) throws Exception {

        if (operatorPassword == null || !operatorPassword.equals(password)) {
            throw new SecurityException();
        }

        Path target = resolveFile(fileKey);
        String output = run(command);
        String digest = buildDigest(label);
        String summary = summarize(reportType, target, output);

        return new Plan(target.toString(), output, digest, summary);
    }

    private Path resolveFile(String key) {
        String selected = fileMap.containsKey(key) ? fileMap.get(key) : "daily.log";
        return root.resolve(selected).normalize();
    }

    private String run(String cmd) throws Exception {
        String safe = cmd != null && cmd.matches("[a-zA-Z0-9_ -]+") ? cmd : "echo";
        Process process = Runtime.getRuntime().exec(new String[]{"sh", "-c", safe});

        StringBuilder out = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {

            String line;
            while ((line = reader.readLine()) != null) {
                if (out.length() > 0) {
                    out.append('\n');
                }
                out.append(line);
            }
        }

        process.waitFor();
        return out.toString();
    }

    private String buildDigest(String value) throws Exception {
        MessageDigest d = MessageDigest.getInstance("SHA-512");
        byte[] h = d.digest(String.valueOf(value).getBytes(StandardCharsets.UTF_8));
        return HexFormat.of().formatHex(h);
    }

    private String summarize(String type, Path file, String output) {
        String safeType = type != null && type.matches("[a-zA-Z0-9_]+") ? type : "daily";
        return safeType + "|" + file.getFileName() + "|" + output.length();
    }

    public static class Plan {
        public final String file;
        public final String output;
        public final String digest;
        public final String summary;

        public Plan(String file, String output, String digest, String summary) {
            this.file = file;
            this.output = output;
            this.digest = digest;
            this.summary = summary;
        }
    }
}
