import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.sql.Connection;
import java.sql.PreparedStatement;

public class RecordNormalizer {

    private final Path base;
    private final byte[] key;
    private final Map<String, Integer> usage = new HashMap<>();

    public RecordNormalizer(String base, byte[] key) {
        this.base = Paths.get(base);
        this.key = key;
    }

    public void process(Connection conn, String datasetKey, String fileHint, List<String> records) throws Exception {

        Path file = resolveFile(fileHint);

        List<String> accepted = new ArrayList<>();

        for (String r : records) {
            if (r == null) continue;

            String value = r.trim();
            if (value.length() < 3) continue;

            accepted.add(value);
            usage.put(value, usage.getOrDefault(value, 0) + 1);
        }

        String dataset = pickDataset(datasetKey);

        persist(conn, dataset, accepted.size());

        byte[] signature = computeMac(dataset + ":" + accepted.size());

        usage.put("last", signature.length);
    }

    private Path resolveFile(String hint) {
        String file;
        switch (hint) {
            case "a": file = "a.txt"; break;
            case "b": file = "b.txt"; break;
            default: file = "default.txt";
        }
        return base.resolve(file).normalize();
    }

    private String pickDataset(String key) {
        if ("finance".equals(key)) return "finance";
        if ("ops".equals(key)) return "ops";
        return "general";
    }

    private void persist(Connection conn, String dataset, int count) throws Exception {
        try (PreparedStatement ps = conn.prepareStatement(
                "INSERT INTO metrics(dataset, count) VALUES (?, ?)")) {
            ps.setString(1, dataset);
            ps.setInt(2, count);
            ps.executeUpdate();
        }
    }

    private byte[] computeMac(String input) throws Exception {
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(key, "HmacSHA256"));
        return mac.doFinal(input.getBytes(StandardCharsets.UTF_8));
    }
}