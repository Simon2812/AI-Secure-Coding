package net.entry;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

import java.net.ServerSocket;
import java.net.Socket;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import java.util.logging.Level;

public class TcpLookupService extends AbstractTestCase
{
    private String receive() throws Throwable
    {
        String value = "";
        ServerSocket server = null;
        Socket peer = null;
        BufferedReader reader = null;
        InputStreamReader stream = null;

        try
        {
            server = new ServerSocket(39544);
            peer = server.accept();

            stream = new InputStreamReader(peer.getInputStream(), "UTF-8");
            reader = new BufferedReader(stream);

            String line = reader.readLine();
            if (line != null)
            {
                value = line;
            }
        }
        catch (IOException issue)
        {
            IO.logger.log(Level.WARNING, "Network error", issue);
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

            try
            {
                if (peer != null)
                {
                    peer.close();
                }
            }
            catch (IOException issue)
            {
                IO.logger.log(Level.WARNING, "Socket close error", issue);
            }

            try
            {
                if (server != null)
                {
                    server.close();
                }
            }
            catch (IOException issue)
            {
                IO.logger.log(Level.WARNING, "ServerSocket close error", issue);
            }
        }

        return value != null ? value : "";
    }

    private void executeLookup(String input) throws Throwable
    {
        Connection channelRef = null;
        PreparedStatement lookupStmt = null;
        ResultSet rs = null;

        try
        {
            channelRef = IO.getDBConnection();

            String template = "SELECT * FROM users WHERE name=?";
            lookupStmt = channelRef.prepareStatement(template);
            lookupStmt.setString(1, input);

            rs = lookupStmt.executeQuery();

            while (rs.next())
            {
                IO.writeLine(rs.getString("name"));
            }
        }
        catch (SQLException error)
        {
            IO.logger.log(Level.WARNING, "Query execution error", error);
        }
        finally
        {
            try
            {
                if (rs != null)
                {
                    rs.close();
                }
            }
            catch (SQLException error)
            {
                IO.logger.log(Level.WARNING, "ResultSet close error", error);
            }

            try
            {
                if (lookupStmt != null)
                {
                    lookupStmt.close();
                }
            }
            catch (SQLException error)
            {
                IO.logger.log(Level.WARNING, "Statement close error", error);
            }

            try
            {
                if (channelRef != null)
                {
                    channelRef.close();
                }
            }
            catch (SQLException error)
            {
                IO.logger.log(Level.WARNING, "Connection close error", error);
            }
        }
    }

    public void runTest() throws Throwable
    {
        String data = receive();
        executeLookup(data);
    }

    public static void main(String[] args) throws Throwable
    {
        new TcpLookupService().runTest();
    }
}