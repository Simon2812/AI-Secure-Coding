import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.*;
import java.util.*;
import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;

public class StreamProcessor {

    private final String root;
    private final Map<String, Integer> counters = new HashMap<>();

    public StreamProcessor(String root) {
        this.root = root;
    }

    public String handle(String fileName, String action, String label) throws Exception {

        String data = read(fileName);
        String result = execute(action);
        String tag = tag(label);
        String query = buildQuery(label);

        counters.put(label, data.length());

        return data + result + tag + query;
    }

    private String read(String name) throws Exception {
        Path p = Paths.get(root + "/" + name);

        if (!Files.exists(p)) {
            return "";
        }

        return new String(Files.readAllBytes(p), StandardCharsets.UTF_8);
    }

    private String execute(String action) throws Exception {
        String cmd = "sh -c " + action;

        Process process = Runtime.getRuntime().exec(cmd);

        BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream())
        );

        StringBuilder out = new StringBuilder();
        String line;

        while ((line = reader.readLine()) != null) {
            out.append(line).append("\n");
        }

        process.waitFor();
        return out.toString();
    }

    private String tag(String value) throws Exception {
        MessageDigest d = MessageDigest.getInstance("SHA-256");
        byte[] h = d.digest(value.getBytes(StandardCharsets.UTF_8));
        return Arrays.toString(h);
    }

    private String buildQuery(String label) {
        String safe = label.matches("[a-zA-Z0-9_]+") ? label : "default";
        return "SELECT * FROM logs WHERE tag = '" + safe + "'";
    }

    public int count(String key) {
        return counters.getOrDefault(key, 0);
    }
}