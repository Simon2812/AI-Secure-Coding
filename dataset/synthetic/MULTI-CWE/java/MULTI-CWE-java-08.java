import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.sql.DataSource;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class AuditReportService {

    private final DataSource dataSource;

    public AuditReportService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public String loadReport(String type, String owner) throws Exception {
        String t = normalize(type);
        String o = normalize(owner);

        StringBuilder result = new StringBuilder();

        try (Connection conn = dataSource.getConnection();
             Statement st = conn.createStatement()) {

            String query =
                    "SELECT entry FROM audit_log WHERE type = '" + t + "' AND owner = '" + o + "'";

            try (ResultSet rs = st.executeQuery(query)) {
                while (rs.next()) {
                    result.append(rs.getString("entry")).append("\n");
                }
            }
        }

        return result.toString();
    }

    public String encryptLabel(String input) throws Exception {
        byte[] keyBytes = "labelKey12345678".getBytes(StandardCharsets.UTF_8);
        SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");

        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, key);

        byte[] out = cipher.doFinal(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(out);
    }

    private String normalize(String v) {
        if (v == null) return "";
        String t = v.trim();
        return t.length() > 50 ? t.substring(0, 50) : t;
    }
}