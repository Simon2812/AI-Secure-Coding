package net.client;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

import java.net.URL;
import java.net.URLConnection;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import java.util.logging.Level;

public class RemoteQueryProcessor extends AbstractTestCase
{
    private String fetchRemoteValue() throws Throwable
    {
        String payload = "";
        URLConnection link = null;
        BufferedReader reader = null;
        InputStreamReader stream = null;

        try
        {
            URL endpoint = new URL("http://example.org/");
            link = endpoint.openConnection();
            stream = new InputStreamReader(link.getInputStream(), "UTF-8");
            reader = new BufferedReader(stream);

            String line = reader.readLine();
            if (line != null)
            {
                payload = line;
            }
        }
        catch (IOException issue)
        {
            IO.logger.log(Level.WARNING, "Remote read error", issue);
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
            catch (IOException issue)
            {
                IO.logger.log(Level.WARNING, "Reader close error", issue);
            }

            try
            {
                if (stream != null)
                {
                    stream.close();
                }
            }
            catch (IOException issue)
            {
                IO.logger.log(Level.WARNING, "Stream close error", issue);
            }
        }

        return payload != null ? payload : "";
    }

    private void executeLookup(String input) throws Throwable
    {
        Connection session = null;
        PreparedStatement queryUnit = null;
        ResultSet results = null;

        try
        {
            session = IO.getDBConnection();

            String sqlTemplate = "SELECT * FROM users WHERE name=?";
            queryUnit = session.prepareStatement(sqlTemplate);
            queryUnit.setString(1, input);

            results = queryUnit.executeQuery();

            while (results.next())
            {
                IO.writeLine(results.getString("name"));
            }
        }
        catch (SQLException problem)
        {
            IO.logger.log(Level.WARNING, "Query error", problem);
        }
        finally
        {
            try
            {
                if (results != null)
                {
                    results.close();
                }
            }
            catch (SQLException problem)
            {
                IO.logger.log(Level.WARNING, "ResultSet close error", problem);
            }

            try
            {
                if (queryUnit != null)
                {
                    queryUnit.close();
                }
            }
            catch (SQLException problem)
            {
                IO.logger.log(Level.WARNING, "Statement close error", problem);
            }

            try
            {
                if (session != null)
                {
                    session.close();
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
        String value = fetchRemoteValue();
        executeLookup(value);
    }

    public static void main(String[] args) throws Throwable
    {
        new RemoteQueryProcessor().runTest();
    }
}