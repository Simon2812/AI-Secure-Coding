package web.handlers;

import juliet.support.AbstractTestCaseServlet;
import juliet.support.IO;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.io.IOException;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import java.util.logging.Level;

public class UserQueryServlet extends AbstractTestCaseServlet
{
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws Throwable, IOException
    {
        String incoming = request.getParameter("username");

        if (incoming == null)
        {
            incoming = "";
        }

        Connection dbSession = null;
        PreparedStatement finder = null;
        ResultSet records = null;

        try
        {
            dbSession = IO.getDBConnection();

            String template = "SELECT * FROM users WHERE name=?";
            finder = dbSession.prepareStatement(template);
            finder.setString(1, incoming);

            records = finder.executeQuery();

            while (records.next())
            {
                IO.writeLine(records.getString("name"));
            }
        }
        catch (SQLException issue)
        {
            IO.logger.log(Level.WARNING, "Query failure", issue);
        }
        finally
        {
            try
            {
                if (records != null)
                {
                    records.close();
                }
            }
            catch (SQLException issue)
            {
                IO.logger.log(Level.WARNING, "ResultSet close failure", issue);
            }

            try
            {
                if (finder != null)
                {
                    finder.close();
                }
            }
            catch (SQLException issue)
            {
                IO.logger.log(Level.WARNING, "Statement close failure", issue);
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
                IO.logger.log(Level.WARNING, "Connection close failure", issue);
            }
        }
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws Throwable, IOException
    {
        doPost(request, response);
    }
}