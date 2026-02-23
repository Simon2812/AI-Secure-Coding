package net.integration;

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

public class RemoteAuditProcessor extends AbstractTestCase
{
    private String acquire() throws Throwable
    {
        String result = "";
        URLConnection remoteLink = null;
        InputStreamReader inputBridge = null;
        BufferedReader buffer = null;

        try
        {
            URL resource = new URL("http://example.org/");
            remoteLink = resource.openConnection();
            remoteLink.setUseCaches(false);
            remoteLink.setDoInput(true);

            inputBridge = new InputStreamReader(remoteLink.getInputStream(), "UTF-8");
            buffer = new BufferedReader(inputBridge);

            String line = buffer.readLine();
            if (line != null)
            {
                result = line.trim();
            }
        }
        catch (IOException ex)
        {
            IO.logger.log(Level.WARNING, "Remote read failure", ex);
        }
        finally
        {
            try
            {
                if (buffer != null)
                {
                    buffer.close();
                }
            }
            catch (IOException ex)
            {
                IO.logger.log(Level.WARNING, "Buffer close failure", ex);
            }

            try
            {
                if (inputBridge != null)
                {
                    inputBridge.close();
                }
            }
            catch (IOException ex)
            {
                IO.logger.log(Level.WARNING, "Stream close failure", ex);
            }
        }

        return result != null ? result : "";
    }

    private void persist(String value) throws Throwable
    {
        Connection transport = null;
        PreparedStatement operator = null;
        ResultSet rs = null;

        try
        {
            transport = IO.getDBConnection();
            transport.setAutoCommit(true);

            String queryForm = "SELECT name FROM users WHERE name=?";
            operator = transport.prepareStatement(queryForm);
            operator.setString(1, value);

            rs = operator.executeQuery();

            while (rs.next())
            {
                IO.writeLine(rs.getString(1));
            }
        }
        catch (SQLException ex)
        {
            IO.logger.log(Level.WARNING, "Database interaction failure", ex);
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
            catch (SQLException ex)
            {
                IO.logger.log(Level.WARNING, "ResultSet close failure", ex);
            }

            try
            {
                if (operator != null)
                {
                    operator.close();
                }
            }
            catch (SQLException ex)
            {
                IO.logger.log(Level.WARNING, "Statement close failure", ex);
            }

            try
            {
                if (transport != null)
                {
                    transport.close();
                }
            }
            catch (SQLException ex)
            {
                IO.logger.log(Level.WARNING, "Connection close failure", ex);
            }
        }
    }

    public void runTest() throws Throwable
    {
        String payload = acquire();
        persist(payload);
    }

    public static void main(String[] args) throws Throwable
    {
        new RemoteAuditProcessor().runTest();
    }
}