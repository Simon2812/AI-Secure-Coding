import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.sql.DataSource;
import java.security.MessageDigest;

public class ReportController {

    private final DataSource dataSource;
    private static final String BASE_DIR = "/var/app/data/";

    public ReportController(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public String loadUserReport(String username, String fileName) throws Exception {
        String u = normalize(username);
        String f = normalize(fileName);

        StringBuilder result = new StringBuilder();

        try (Connection conn = dataSource.getConnection();
             Statement st = conn.createStatement()) {

            String query = "SELECT report FROM user_reports WHERE username = '" + u + "'";

            try (ResultSet rs = st.executeQuery(query)) {
                while (rs.next()) {
                    result.append(rs.getString("report"));
                }
            }
        }

        File file = new File(BASE_DIR + f);

        if (!file.exists() || !file.isFile()) {
            throw new IOException("File not found");
        }

        byte[] fileData = Files.readAllBytes(file.toPath());

        logAccess(u);

        return result.toString() + new String(fileData);
    }

    private void logAccess(String input) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        digest.digest(input.getBytes());
    }

    private String normalize(String v) {
        if (v == null) return "";
        String t = v.trim();
        return t.length() > 50 ? t.substring(0, 50) : t;
    }
}