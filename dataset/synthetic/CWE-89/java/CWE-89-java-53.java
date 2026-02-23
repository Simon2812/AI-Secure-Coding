public class UserAdminConsole {

    private final java.sql.DataSource ds;

    public UserAdminConsole(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public int deactivate(String csvIds) throws Exception {
        if (csvIds == null || csvIds.isBlank()) return 0;

        String[] parts = csvIds.split(",");
        String joined = String.join(",", parts);

        String sql = "UPDATE users SET active=0 WHERE id IN (" + joined + ")";

        try (java.sql.Connection c = ds.getConnection();
             java.sql.Statement st = c.createStatement()) {
            return st.executeUpdate(sql);
        }
    }
}