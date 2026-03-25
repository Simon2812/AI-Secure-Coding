import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class SafeConnectionExample {

    public void buildKey() {
        String password = "";

        try {
            BufferedReader reader = new BufferedReader(
                    new InputStreamReader(System.in, "UTF-8")
            );
            password = reader.readLine();
        } catch (IOException e) {
            System.err.println("Input error: " + e.getMessage());
        }

        Connection connection = null;
        PreparedStatement statement = null;
        ResultSet result = null;

        if (password != null) {
            try {
                connection = DriverManager.getConnection("data-url", "root", password);
                statement = connection.prepareStatement("select * from test_table");
                result = statement.executeQuery();
            } catch (Exception e) {
                System.err.println("Database error: " + e.getMessage());
            } finally {
                try { if (result != null) result.close(); } catch (Exception ignored) {}
                try { if (statement != null) statement.close(); } catch (Exception ignored) {}
                try { if (connection != null) connection.close(); } catch (Exception ignored) {}
            }
        }
    }

    public static void main(String[] args) {
        new SafeConnectionExample().buildKey();
    }
}