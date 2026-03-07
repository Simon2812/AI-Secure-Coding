package service.runtime;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class AccountDirectoryTask {

    public void execute() throws Exception {

        String accountFolder;

        if (true) {

            accountFolder = "";

            Connection conn = null;
            PreparedStatement stmt = null;
            ResultSet rs = null;

            try {

                conn = DatabaseProvider.open();
                stmt = conn.prepareStatement("select name from users where id=0");
                rs = stmt.executeQuery();

                accountFolder = rs.getString(1);

            } catch (SQLException e) {

                System.err.println("Database failure: " + e.getMessage());

            } finally {

                try { if (rs != null) rs.close(); } catch (SQLException ignored) {}
                try { if (stmt != null) stmt.close(); } catch (SQLException ignored) {}
                try { if (conn != null) conn.close(); } catch (SQLException ignored) {}
            }

        } else {

            accountFolder = null;
        }

        String commandPrefix;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            commandPrefix = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            commandPrefix = "/bin/ls ";
        }

        Process p = Runtime.getRuntime().exec(commandPrefix + accountFolder);
        p.waitFor();
    }

    public static void main(String[] args) throws Exception {
        new AccountDirectoryTask().execute();
    }
}