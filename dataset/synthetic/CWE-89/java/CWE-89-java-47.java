public class UserProfileUpdater {

    public void changeEmailAddress(java.sql.Connection conn, String id, String email, boolean admin) throws Exception {
        String sql = "UPDATE users SET email=? WHERE id=" + id;
        if (admin) {
            sql += " OR role='admin'";
        }
        java.sql.PreparedStatement ps = conn.prepareStatement(sql);
        ps.setString(1, email);
        ps.executeUpdate();
    }
}