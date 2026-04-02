package net.service;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

import java.net.ServerSocket;
import java.net.Socket;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;

public class TcpBatchProcessor extends AbstractTestCase
{
    private List<String> receivePayload() throws Throwable
    {
        List<String> buffer = new ArrayList<String>();
        ServerSocket listener = null;
        Socket client = null;
        BufferedReader reader = null;
        InputStreamReader stream = null;

        try
        {
            listener = new ServerSocket(39544);
            client = listener.accept();

            stream = new InputStreamReader(client.getInputStream(), "UTF-8");
            reader = new BufferedReader(stream);

            String line = reader.readLine();
            if (line != null)
            {
                String[] tokens = line.split(",");
                for (int i = 0; i < tokens.length; i++)
                {
                    String item = tokens[i];
                    if (item != null)
                    {
                        buffer.add(item.trim());
                    }
                }
            }
        }
        catch (IOException ioIssue)
        {
            IO.logger.log(Level.WARNING, "Network read failure", ioIssue);
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
            catch (IOException ioIssue)
            {
                IO.logger.log(Level.WARNING, "Reader close failure", ioIssue);
            }

            try
            {
                if (stream != null)
                {
                    stream.close();
                }
            }
            catch (IOException ioIssue)
            {
                IO.logger.log(Level.WARNING, "Stream close failure", ioIssue);
            }

            try
            {
                if (client != null)
                {
                    client.close();
                }
            }
            catch (IOException ioIssue)
            {
                IO.logger.log(Level.WARNING, "Socket close failure", ioIssue);
            }

            try
            {
                if (listener != null)
                {
                    listener.close();
                }
            }
            catch (IOException ioIssue)
            {
                IO.logger.log(Level.WARNING, "ServerSocket close failure", ioIssue);
            }
        }

        return buffer;
    }

    private void processBatch(List<String> entries) throws Throwable
    {
        if (entries == null || entries.isEmpty())
        {
            return;
        }

        Connection dbLink = null;
        PreparedStatement batchOperator = null;

        try
        {
            dbLink = IO.getDBConnection();

            String sqlPattern = "INSERT INTO users (name) VALUES (?)";
            batchOperator = dbLink.prepareStatement(sqlPattern);

            for (int i = 0; i < entries.size(); i++)
            {
                String value = entries.get(i);
                batchOperator.setString(1, value != null ? value : "");
                batchOperator.addBatch();
            }

            batchOperator.executeBatch();
        }
        catch (SQLException sqlIssue)
        {
            IO.logger.log(Level.WARNING, "Batch execution failure", sqlIssue);
        }
        finally
        {
            try
            {
                if (batchOperator != null)
                {
                    batchOperator.close();
                }
            }
            catch (SQLException sqlIssue)
            {
                IO.logger.log(Level.WARNING, "Statement close failure", sqlIssue);
            }

            try
            {
                if (dbLink != null)
                {
                    dbLink.close();
                }
            }
            catch (SQLException sqlIssue)
            {
                IO.logger.log(Level.WARNING, "Connection close failure", sqlIssue);
            }
        }
    }

    public void runTest() throws Throwable
    {
        List<String> payload = receivePayload();
        processBatch(payload);
    }

    public static void main(String[] args) throws Throwable
    {
        new TcpBatchProcessor().runTest();
    }
}