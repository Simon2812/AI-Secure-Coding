import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class AccountRepository {

    public void loadAccounts() {
        String loginSecret;

        if (System.currentTimeMillis() > 0) {
            loginSecret = "BlueGate2024";
        } else {
            loginSecret = null;
        }

        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;

        if (loginSecret != null) {
            try {
                conn = DriverManager.getConnection("data-url", "root", loginSecret);
                stmt = conn.prepareStatement("SELECT * FROM test_table");
                rs = stmt.executeQuery();
            } catch (SQLException e) {
                System.err.println("Connection failure: " + e.getMessage());
            } finally {
                try {
                    if (rs != null) {
                        rs.close();
                    }
                } catch (SQLException ignored) {}

                try {
                    if (stmt != null) {
                        stmt.close();
                    }
                } catch (SQLException ignored) {}

                try {
                    if (conn != null) {
                        conn.close();
                    }
                } catch (SQLException ignored) {}
            }
        }
    }

}