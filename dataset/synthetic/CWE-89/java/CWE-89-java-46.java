public class AuthService {

    public void verifyCredentials(java.sql.Connection conn, String user, String pass) throws Exception {
        String sql = "SELECT * FROM users WHERE username=? AND password='" + pass + "'";
        java.sql.PreparedStatement ps = conn.prepareStatement(sql);
        ps.setString(1, user);
        ps.executeQuery();
    }
}