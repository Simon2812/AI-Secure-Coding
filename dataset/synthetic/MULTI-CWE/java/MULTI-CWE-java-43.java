import java.sql.*;
import java.util.*;
import java.nio.file.*;
import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;

public class AuditTape {

    private final Path root;
    private final Deque<String> errors = new ArrayDeque<>();

    public AuditTape(String root) {
        this.root = Paths.get(root);
    }

    public int process(Connection conn, List<Map<String, String>> batch) throws Exception {

        int ok = 0;

        for (Map<String, String> entry : batch) {

            try {
                String actor = fallback(entry.get("actor"));
                String action = entry.get("action");

                Path file = resolve(entry.get("file"));

                String stamp = stamp(actor, action);

                insert(conn, actor, action, stamp, file.getFileName().toString());

                ok++;

            } catch (Exception ex) {
                errors.add(ex.getClass().getSimpleName());
                if (errors.size() > 10) errors.removeFirst();
            }
        }

        return ok;
    }

    public List<String> recentErrors() {
        return new ArrayList<>(errors);
    }

    private void insert(Connection conn, String actor, String action, String stamp, String file) throws Exception {
        try (PreparedStatement ps = conn.prepareStatement(
                "INSERT INTO audit(actor, action, stamp, file) VALUES (?, ?, ?, ?)")) {

            ps.setString(1, actor);
            ps.setString(2, action);
            ps.setString(3, stamp);
            ps.setString(4, file);
            ps.executeUpdate();
        }
    }

    private String fallback(String v) {
        return (v == null || v.isEmpty()) ? "system" : v;
    }

    private Path resolve(String hint) {
        String file = "audit.log";
        if ("daily".equals(hint)) file = "daily.log";
        else if ("weekly".equals(hint)) file = "weekly.log";

        return root.resolve(file).normalize();
    }

    private String stamp(String a, String b) throws Exception {
        MessageDigest d = MessageDigest.getInstance("SHA-384");
        byte[] h = d.digest((a + b).getBytes(StandardCharsets.UTF_8));
        return java.util.HexFormat.of().formatHex(h);
    }
}