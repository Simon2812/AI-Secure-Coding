public class SessionLookup {

    private final java.sql.DataSource ds;

    public SessionLookup(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public String findOwner(String token) throws Exception {
        if (token == null || token.isBlank()) return null;

        String sql = "SELECT user_id FROM sessions WHERE token=?";

        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {

            ps.setString(1, token);
            try (java.sql.ResultSet rs = ps.executeQuery()) {
                return rs.next() ? rs.getString(1) : null;
            }
        }
    }
}