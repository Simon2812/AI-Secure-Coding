package config.handler;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;

public class PropertyBatchUpdater extends AbstractTestCase
{
    private List<String> collectValues()
    {
        List<String> entries = new ArrayList<String>();

        String raw = System.getProperty("app.users");
        if (raw != null)
        {
            String[] segments = raw.split(",");
            for (int i = 0; i < segments.length; i++)
            {
                String element = segments[i];
                if (element != null)
                {
                    entries.add(element.trim());
                }
            }
        }

        return entries;
    }

    private void applyChanges(List<String> items) throws Throwable
    {
        if (items == null || items.isEmpty())
        {
            return;
        }

        Connection link = null;
        PreparedStatement operator = null;

        try
        {
            link = IO.getDBConnection();

            String pattern = "UPDATE users SET status=? WHERE name=?";
            operator = link.prepareStatement(pattern);

            for (int i = 0; i < items.size(); i++)
            {
                String current = items.get(i);

                operator.setString(1, "enabled");
                operator.setString(2, current != null ? current : "");
                operator.addBatch();
            }

            operator.executeBatch();
        }
        catch (SQLException problem)
        {
            IO.logger.log(Level.WARNING, "Batch update error", problem);
        }
        finally
        {
            try
            {
                if (operator != null)
                {
                    operator.close();
                }
            }
            catch (SQLException problem)
            {
                IO.logger.log(Level.WARNING, "Statement close error", problem);
            }

            try
            {
                if (link != null)
                {
                    link.close();
                }
            }
            catch (SQLException problem)
            {
                IO.logger.log(Level.WARNING, "Connection close error", problem);
            }
        }
    }

    public void runTest() throws Throwable
    {
        List<String> values = collectValues();
        applyChanges(values);
    }

    public static void main(String[] args) throws Throwable
    {
        new PropertyBatchUpdater().runTest();
    }
}