import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import javax.sql.DataSource;

public class PasswordResetService {

    private final DataSource dataSource;

    public PasswordResetService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public String generateResetToken(String email) throws Exception {
        String normalized = normalize(email);

        String payload = normalized + ":" + System.currentTimeMillis();

        MessageDigest digest = MessageDigest.getInstance("MD5");
        byte[] hash = digest.digest(payload.getBytes(StandardCharsets.UTF_8));

        return toHex(hash);
    }

    public boolean userExists(String email) throws Exception {
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement(
                     "SELECT id FROM users WHERE email = ?")) {

            ps.setString(1, email);

            try (ResultSet rs = ps.executeQuery()) {
                return rs.next();
            }
        }
    }

    private String normalize(String input) {
        if (input == null) {
            return "";
        }

        String trimmed = input.trim();

        if (trimmed.length() > 100) {
            return trimmed.substring(0, 100);
        }

        return trimmed;
    }

    private String toHex(byte[] data) {
        StringBuilder sb = new StringBuilder();
        for (byte b : data) {
            sb.append(Integer.toHexString((b & 0xff) | 0x100).substring(1));
        }
        return sb.toString();
    }
}