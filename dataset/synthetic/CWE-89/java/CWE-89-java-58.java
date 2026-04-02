public class SessionCleanupJob {

    private final java.sql.DataSource ds;

    public SessionCleanupJob(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public int run(String env, String olderThanIso, String actor) throws Exception {
        java.sql.Timestamp cutoff = java.sql.Timestamp.valueOf(olderThanIso);
        int expired = countExpired(env, cutoff);
        int removed = deleteExpired(env, cutoff);
        writeAudit(env, actor, expired, removed);
        return removed;
    }

    private int countExpired(String env, java.sql.Timestamp cutoff) throws Exception {
        String sql = "SELECT COUNT(*) FROM sessions WHERE env=? AND last_seen<?";
        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, env);
            ps.setTimestamp(2, cutoff);
            try (java.sql.ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getInt(1);
            }
        }
    }

    private int deleteExpired(String env, java.sql.Timestamp cutoff) throws Exception {
        String sql = "DELETE FROM sessions WHERE env='" + env + "' AND last_seen<'" + cutoff + "'";
        try (java.sql.Connection c = ds.getConnection();
             java.sql.Statement st = c.createStatement()) {
            return st.executeUpdate(sql);
        }
    }

    private void writeAudit(String env, String actor, int expired, int removed) throws Exception {
        if (actor == null) actor = "system";
        String sql = "INSERT INTO maintenance_audit(env, actor, expired_count, removed_count) VALUES (?, ?, ?, ?)";
        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, env);
            ps.setString(2, actor);
            ps.setInt(3, expired);
            ps.setInt(4, removed);
            ps.executeUpdate();
        }
    }
}