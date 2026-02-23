public class UserLookupService {

    public void loadUserByEmail(java.sql.Connection conn, String email) throws Exception {
        String sql = "SELECT id FROM users WHERE email = '" + email + "'";
        java.sql.Statement st = conn.createStatement();
        st.executeQuery(sql);
    }
}