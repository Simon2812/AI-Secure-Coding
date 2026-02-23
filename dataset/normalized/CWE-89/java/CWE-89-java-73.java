package config.update;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.util.logging.Level;

public class PropertyStatusUpdater extends AbstractTestCase
{
    private String readConfig()
    {
        String content = System.getProperty("service.user");
        if (content == null)
        {
            content = "";
        }
        return content;
    }

    private void performUpdate(String input) throws Throwable
    {
        if (input == null)
        {
            input = "";
        }

        Connection dbSession = null;
        PreparedStatement command = null;

        try
        {
            dbSession = IO.getDBConnection();

            String template = "UPDATE users SET status=? WHERE name=?";
            command = dbSession.prepareStatement(template);

            command.setString(1, "processed");
            command.setString(2, input);

            command.executeUpdate();
        }
        catch (SQLException issue)
        {
            IO.logger.log(Level.WARNING, "Update error", issue);
        }
        finally
        {
            try
            {
                if (command != null)
                {
                    command.close();
                }
            }
            catch (SQLException issue)
            {
                IO.logger.log(Level.WARNING, "Statement close error", issue);
            }

            try
            {
                if (dbSession != null)
                {
                    dbSession.close();
                }
            }
            catch (SQLException issue)
            {
                IO.logger.log(Level.WARNING, "Connection close error", issue);
            }
        }
    }

    public void runTest() throws Throwable
    {
        String value = readConfig();
        performUpdate(value);
    }

    public static void main(String[] args) throws Throwable
    {
        new PropertyStatusUpdater().runTest();
    }
}