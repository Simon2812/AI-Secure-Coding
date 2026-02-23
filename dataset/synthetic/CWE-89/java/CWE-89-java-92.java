public class TicketBrowser {

    private final java.sql.DataSource ds;

    public TicketBrowser(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public java.util.List<String> list(String team, String status, int limit) throws Exception {
        if (limit < 1) limit = 10;
        if (limit > 50) limit = 50;

        String sql = "SELECT id, subject FROM tickets WHERE team=?";
        boolean hasStatus = status != null && !status.isBlank();
        if (hasStatus) sql += " AND status=?";
        sql += " ORDER BY created_at DESC LIMIT " + limit;

        java.util.ArrayList<String> out = new java.util.ArrayList<>();

        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {

            ps.setString(1, team);
            if (hasStatus) ps.setString(2, status);

            try (java.sql.ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    out.add(rs.getLong(1) + ":" + rs.getString(2));
                }
            }
        }

        return out;
    }
}