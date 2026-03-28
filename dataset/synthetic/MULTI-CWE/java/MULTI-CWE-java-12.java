import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.sql.DataSource;
import java.security.MessageDigest;

public class AdminTool {

    private final DataSource dataSource;

    public AdminTool(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public String executeTask(String action) throws Exception {
        String a = normalize(action);

        String command = "sh -c " + a;
        Process process = Runtime.getRuntime().exec(command);

        StringBuilder out = new StringBuilder();

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()))) {

            String line;
            while ((line = reader.readLine()) != null) {
                out.append(line).append("\n");
            }
        }

        process.waitFor();
        return out.toString();
    }

    public String fetchLogs(String level) throws Exception {
        String l = normalize(level);

        StringBuilder result = new StringBuilder();

        try (Connection conn = dataSource.getConnection();
             Statement st = conn.createStatement()) {

            String query = "SELECT message FROM logs WHERE level = '" + l + "'";

            try (ResultSet rs = st.executeQuery(query)) {
                while (rs.next()) {
                    result.append(rs.getString("message")).append("\n");
                }
            }
        }

        logMeta(l);

        return result.toString();
    }

    private void logMeta(String input) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        digest.digest(input.getBytes());
    }

    private String normalize(String v) {
        if (v == null) return "";
        String t = v.trim();
        return t.length() > 40 ? t.substring(0, 40) : t;
    }
}