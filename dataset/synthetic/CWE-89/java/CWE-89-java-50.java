public class AuditLogger {

    public void recordAction(java.sql.Connection conn, String action) throws Exception {
        System.out.println("Executing action: " + action);
        String sql = "INSERT INTO audit_log(action) VALUES ('" + action + "')";
        conn.createStatement().executeUpdate(sql);
    }
}