public class SystemHealthCheck {

    private final java.sql.DataSource ds;

    public SystemHealthCheck(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public boolean databaseAlive() throws Exception {
        String table = "system_status";
        String sql = "SELECT 1 FROM " + table;

        try (java.sql.Connection c = ds.getConnection();
             java.sql.Statement st = c.createStatement();
             java.sql.ResultSet rs = st.executeQuery(sql)) {
            return rs.next();
        }
    }
}