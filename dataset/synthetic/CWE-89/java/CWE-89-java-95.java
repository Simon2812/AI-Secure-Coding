public class AuditAppender {

    private final java.sql.DataSource ds;

    public AuditAppender(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public void append(String actor, String action, String details) throws Exception {
        String who = actor == null ? "unknown" : actor;
        String what = action == null ? "" : action;
        String extra = details == null ? "" : details;

        String sql = "INSERT INTO audit_log(actor, action, details) VALUES (?, ?, ?)";

        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {

            ps.setString(1, who);
            ps.setString(2, what);
            ps.setString(3, extra);
            ps.executeUpdate();
        }
    }
}