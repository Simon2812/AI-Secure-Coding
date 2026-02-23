public class SupportTicketQuery {

    private final java.sql.DataSource ds;

    public SupportTicketQuery(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public java.util.List<String> recent(String team, String status, int limit) throws Exception {
        if (limit < 1) limit = 10;
        if (limit > 50) limit = 50;

        String sql = "SELECT id, subject, status FROM tickets WHERE team='" + team + "'";
        if (status != null && !status.isBlank()) {
            sql += " AND status='" + status + "'";
        }
        sql += " ORDER BY created_at DESC LIMIT " + limit;

        java.util.ArrayList<String> out = new java.util.ArrayList<>();

        try (java.sql.Connection c = ds.getConnection();
             java.sql.Statement st = c.createStatement();
             java.sql.ResultSet rs = st.executeQuery(sql)) {

            while (rs.next()) {
                out.add(rs.getLong(1) + " " + rs.getString(2) + " " + rs.getString(3));
            }
        }

        return out;
    }

    public long countOpen(String team) throws Exception {
        String sql = "SELECT COUNT(*) FROM tickets WHERE team=? AND status=?";
        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, team);
            ps.setString(2, "OPEN");
            try (java.sql.ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getLong(1);
            }
        }
    }
}