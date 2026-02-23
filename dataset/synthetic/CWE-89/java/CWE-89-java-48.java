public class AuditCleanupService {

    public void cleanupUserLogs(java.sql.Connection conn, String userId) throws Exception {
        String lookup = "SELECT nickname FROM profiles WHERE id=?";
        java.sql.PreparedStatement ps = conn.prepareStatement(lookup);
        ps.setString(1, userId);
        java.sql.ResultSet rs = ps.executeQuery();
        if (rs.next()) {
            String nickname = rs.getString(1);
            String sql = "DELETE FROM logs WHERE owner='" + nickname + "'";
            conn.createStatement().executeUpdate(sql);
        }
    }
}