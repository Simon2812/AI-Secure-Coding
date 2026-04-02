package processing.layer;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;

public class BatchUserInsert extends AbstractTestCase
{
    private List<String> loadEntries()
    {
        List<String> values = new ArrayList<String>();
        BufferedReader reader = null;

        try
        {
            reader = new BufferedReader(new FileReader("data.txt"));
            String line;
            while ((line = reader.readLine()) != null)
            {
                if (line.length() > 0)
                {
                    values.add(line);
                }
            }
        }
        catch (IOException exceptIO)
        {
            IO.logger.log(Level.WARNING, "File read error", exceptIO);
        }
        finally
        {
            try
            {
                if (reader != null)
                {
                    reader.close();
                }
            }
            catch (IOException exceptIO)
            {
                IO.logger.log(Level.WARNING, "Reader close error", exceptIO);
            }
        }

        return values;
    }

    private void executeBatchInsert(List<String> entries) throws Throwable
    {
        if (entries == null || entries.isEmpty())
        {
            return;
        }

        Connection connection = null;
        PreparedStatement statement = null;

        try
        {
            connection = IO.getDBConnection();

            String sql = "INSERT INTO users (name) VALUES (?)";
            statement = connection.prepareStatement(sql);

            for (String value : entries)
            {
                statement.setString(1, value != null ? value : "");
                statement.addBatch();
            }

            statement.executeBatch();
        }
        catch (SQLException exceptSql)
        {
            IO.logger.log(Level.WARNING, "Batch execution error", exceptSql);
        }
        finally
        {
            try
            {
                if (statement != null)
                {
                    statement.close();
                }
            }
            catch (SQLException exceptSql)
            {
                IO.logger.log(Level.WARNING, "Statement close error", exceptSql);
            }

            try
            {
                if (connection != null)
                {
                    connection.close();
                }
            }
            catch (SQLException exceptSql)
            {
                IO.logger.log(Level.WARNING, "Connection close error", exceptSql);
            }
        }
    }

    public void runTest() throws Throwable
    {
        List<String> items = loadEntries();
        executeBatchInsert(items);
    }

    public static void main(String[] args) throws Throwable
    {
        new BatchUserInsert().runTest();
    }
}