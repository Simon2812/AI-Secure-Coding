package backend.audit;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class UserDirectoryLookup {

    public void runTask() throws Exception {

        String folderName = "";

        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;

        try {

            conn = DatabaseProvider.getConnection();
            stmt = conn.prepareStatement("select name from users where id=0");
            rs = stmt.executeQuery();

            folderName = rs.getString(1);

        } catch (SQLException e) {

            System.err.println("Database error: " + e.getMessage());

        } finally {

            try { if (rs != null) rs.close(); } catch (SQLException ignored) {}
            try { if (stmt != null) stmt.close(); } catch (SQLException ignored) {}
            try { if (conn != null) conn.close(); } catch (SQLException ignored) {}
        }

        String commandBase;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            commandBase = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            commandBase = "/bin/ls ";
        }

        Process p = Runtime.getRuntime().exec(commandBase + folderName);
        p.waitFor();
    }

    public static void main(String[] args) throws Exception {
        new UserDirectoryLookup().runTask();
    }
}