import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class DatabaseLookupService {

    public void executeQuery() {
        String authValue = "SunsetKey#84";

        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;

        if (authValue != null) {
            try {
                conn = DriverManager.getConnection("data-url", "root", authValue);
                stmt = conn.prepareStatement("SELECT * FROM test_table");
                rs = stmt.executeQuery();
            } catch (SQLException e) {
                System.err.println("Database error: " + e.getMessage());
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

    public static void main(String[] args) {
        new DatabaseLookupService().executeQuery();
    }
}