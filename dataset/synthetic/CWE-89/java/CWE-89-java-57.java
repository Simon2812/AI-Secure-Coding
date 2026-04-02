public class LoginAuditRepository {

    private final java.sql.DataSource ds;

    public LoginAuditRepository(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public boolean lockUser(String operatorId, String userId, String reason) throws Exception {
        if (operatorId == null || userId == null) return false;

        String cleanedReason = reason == null ? "" : reason.trim();

        try (java.sql.Connection c = ds.getConnection()) {
            c.setAutoCommit(false);

            if (!isOperatorAllowed(c, operatorId)) {
                c.rollback();
                return false;
            }

            long updated = applyLock(c, userId, cleanedReason);
            writeAudit(c, operatorId, userId, updated > 0);

            c.commit();
            return updated > 0;
        }
    }

    private boolean isOperatorAllowed(java.sql.Connection c, String operatorId) throws Exception {
        String sql = "SELECT role FROM operators WHERE id=?";

        try (java.sql.PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, operatorId);
            try (java.sql.ResultSet rs = ps.executeQuery()) {
                if (!rs.next()) return false;
                String role = rs.getString(1);
                return "admin".equalsIgnoreCase(role) || "security".equalsIgnoreCase(role);
            }
        }
    }

    private long applyLock(java.sql.Connection c, String userId, String reason) throws Exception {
        String sql = "UPDATE users SET locked=1, lock_reason='" + reason + "' WHERE id='" + userId + "'";

        try (java.sql.Statement st = c.createStatement()) {
            return st.executeUpdate(sql);
        }
    }

    private void writeAudit(java.sql.Connection c, String operatorId, String userId, boolean success) throws Exception {
        String sql = "INSERT INTO security_audit(operator_id, target_user, action, success) VALUES (?, ?, ?, ?)";

        try (java.sql.PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, operatorId);
            ps.setString(2, userId);
            ps.setString(3, "LOCK_USER");
            ps.setBoolean(4, success);
            ps.executeUpdate();
        }
    }

    public java.util.List<String> listLockedUsers(int limit) throws Exception {
        if (limit < 1) limit = 10;

        String sql = "SELECT id, lock_reason FROM users WHERE locked=1 ORDER BY id";

        java.util.ArrayList<String> out = new java.util.ArrayList<>();

        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql);
             java.sql.ResultSet rs = ps.executeQuery()) {

            int count = 0;
            while (rs.next() && count < limit) {
                out.add(rs.getString(1) + ":" + rs.getString(2));
                count++;
            }
        }

        return out;
    }

    public boolean unlockUser(String operatorId, String userId) throws Exception {
        if (operatorId == null || userId == null) return false;

        try (java.sql.Connection c = ds.getConnection()) {
            c.setAutoCommit(false);

            if (!isOperatorAllowed(c, operatorId)) {
                c.rollback();
                return false;
            }

            String sql = "UPDATE users SET locked=0, lock_reason=NULL WHERE id=?";
            long updated;
            try (java.sql.PreparedStatement ps = c.prepareStatement(sql)) {
                ps.setString(1, userId);
                updated = ps.executeUpdate();
            }

            writeAudit(c, operatorId, userId, updated > 0);
            c.commit();
            return updated > 0;
        }
    }
}