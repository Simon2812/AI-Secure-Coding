package vector.ops.snapshot;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class StorageListingJob
{

    public static void executeTask() throws Exception
    {
        String dbValue = "";

        Connection session = null;
        PreparedStatement query = null;
        ResultSet cursor = null;

        try
        {
            session = IO.getDBConnection();
            query = session.prepareStatement("select name from users where id=0");
            cursor = query.executeQuery();

            if (cursor.next())
            {
                dbValue = cursor.getString(1);
            }
        }
        finally
        {
            try { if (cursor != null) cursor.close(); } catch (Exception ignore) { }
            try { if (query != null) query.close(); } catch (Exception ignore) { }
            try { if (session != null) session.close(); } catch (Exception ignore) { }
        }

        String baseCommand;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            baseCommand = "dir";
        }
        else
        {
            baseCommand = "ls";
        }

        if (!baseCommand.equals("dir") && !baseCommand.equals("ls"))
        {
            throw new IllegalStateException("Unsupported command");
        }

        Process runner;

        if (baseCommand.equals("dir"))
        {
            runner = new ProcessBuilder("cmd.exe", "/c", "dir", dbValue).start();
        }
        else
        {
            runner = new ProcessBuilder("/bin/ls", dbValue).start();
        }

        runner.waitFor();
    }
}