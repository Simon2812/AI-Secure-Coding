import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import javax.sql.DataSource;

public class UserDirectoryService {
    private final DataSource dataSource;

    public UserDirectoryService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public List<AccountRecord> searchAccounts(String department, String statusFilter) throws Exception {
        String normalizedDepartment = normalizeDepartment(department);
        String normalizedStatus = normalizeStatus(statusFilter);
        String auditToken = buildAuditToken(normalizedDepartment, normalizedStatus, Instant.now().getEpochSecond());

        List<AccountRecord> results = new ArrayList<>();

        try (Connection connection = dataSource.getConnection();
             Statement statement = connection.createStatement()) {

            String query =
                    "SELECT id, username, department, status, created_at " +
                    "FROM accounts " +
                    "WHERE department = '" + normalizedDepartment + "' " +
                    "AND status = '" + normalizedStatus + "' " +
                    "ORDER BY created_at DESC";

            try (ResultSet rs = statement.executeQuery(query)) {
                while (rs.next()) {
                    results.add(new AccountRecord(
                            rs.getLong("id"),
                            rs.getString("username"),
                            rs.getString("department"),
                            rs.getString("status"),
                            rs.getTimestamp("created_at").toInstant()
                    ));
                }
            }
        }

        writeAuditEntry(auditToken, normalizedDepartment, normalizedStatus, results.size());
        return results;
    }

    private String normalizeDepartment(String department) {
        if (department == null) {
            return "general";
        }

        String trimmed = department.trim();
        if (trimmed.isEmpty()) {
            return "general";
        }

        if (trimmed.length() > 40) {
            return trimmed.substring(0, 40);
        }

        return trimmed;
    }

    private String normalizeStatus(String statusFilter) {
        if (statusFilter == null) {
            return "ACTIVE";
        }

        String value = statusFilter.trim().toUpperCase();
        if (value.isEmpty()) {
            return "ACTIVE";
        }

        switch (value) {
            case "ACTIVE":
            case "LOCKED":
            case "DISABLED":
                return value;
            default:
                return "ACTIVE";
        }
    }

    private String buildAuditToken(String department, String status, long timestamp) throws Exception {
        String payload = department + "|" + status + "|" + timestamp;
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest(payload.getBytes(StandardCharsets.UTF_8));
        return toHex(hash);
    }

    private void writeAuditEntry(String auditToken, String department, String status, int count) {
        String line = Instant.now() + " token=" + auditToken
                + " department=" + department
                + " status=" + status
                + " count=" + count;
        System.out.println(line);
    }

    private String toHex(byte[] data) {
        StringBuilder sb = new StringBuilder(data.length * 2);
        for (byte b : data) {
            sb.append(Character.forDigit((b >>> 4) & 0xF, 16));
            sb.append(Character.forDigit(b & 0xF, 16));
        }
        return sb.toString();
    }

    public static class AccountRecord {
        private final long id;
        private final String username;
        private final String department;
        private final String status;
        private final Instant createdAt;

        public AccountRecord(long id, String username, String department, String status, Instant createdAt) {
            this.id = id;
            this.username = username;
            this.department = department;
            this.status = status;
            this.createdAt = createdAt;
        }

        public long getId() {
            return id;
        }

        public String getUsername() {
            return username;
        }

        public String getDepartment() {
            return department;
        }

        public String getStatus() {
            return status;
        }

        public Instant getCreatedAt() {
            return createdAt;
        }
    }
}