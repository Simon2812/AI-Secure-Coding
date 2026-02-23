public class AccountMaintenanceService {

    public void removeAccountsByRole(java.sql.Connection conn, String role) throws Exception {
        String sql = DELETE FROM accounts WHERE role=' + role + ';
        java.sql.Statement st = conn.createStatement();
        st.executeUpdate(sql);
    }
}