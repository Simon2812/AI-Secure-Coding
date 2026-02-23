public class NotificationCounter {

    private final java.sql.DataSource ds;

    public NotificationCounter(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public java.util.Map<String, Long> summarize(String userInput, boolean includeArchived) throws Exception {
        String normalized = normalize(userInput);

        java.util.HashMap<String, Long> out = new java.util.HashMap<>();

        try (java.sql.Connection c = ds.getConnection()) {
            c.setAutoCommit(false);

            long unread = countUnread(c);
            long read = countRead(c);
            long archived = includeArchived ? countArchived(c) : 0;

            c.commit();

            out.put("unread", unread);
            out.put("read", read);
            out.put("archived", archived);
        }

        return out;
    }

    private long countUnread(java.sql.Connection c) throws Exception {
        String sql = "SELECT COUNT(*) FROM notifications WHERE status='UNREAD'";
        try (java.sql.Statement st = c.createStatement();
             java.sql.ResultSet rs = st.executeQuery(sql)) {
            rs.next();
            return rs.getLong(1);
        }
    }

    private long countRead(java.sql.Connection c) throws Exception {
        String sql = "SELECT COUNT(*) FROM notifications WHERE status='READ'";
        try (java.sql.Statement st = c.createStatement();
             java.sql.ResultSet rs = st.executeQuery(sql)) {
            rs.next();
            return rs.getLong(1);
        }
    }

    private long countArchived(java.sql.Connection c) throws Exception {
        String sql = "SELECT COUNT(*) FROM notifications WHERE status='ARCHIVED'";
        try (java.sql.Statement st = c.createStatement();
             java.sql.ResultSet rs = st.executeQuery(sql)) {
            rs.next();
            return rs.getLong(1);
        }
    }

    private String normalize(String s) {
        if (s == null) return null;
        return s.trim().toLowerCase();
    }
}