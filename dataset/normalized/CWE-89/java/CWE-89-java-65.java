package web.layer;

import juliet.support.AbstractTestCaseServlet;
import juliet.support.IO;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Cookie;

import java.io.IOException;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.util.logging.Level;

public class CookieActionServlet extends AbstractTestCaseServlet
{
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws Throwable, IOException
    {
        String input = "";

        Cookie[] cookieArray = request.getCookies();
        if (cookieArray != null)
        {
            for (Cookie c : cookieArray)
            {
                if ("SessionId".equals(c.getName()))
                {
                    input = c.getValue();
                    break;
                }
            }
        }

        if (input == null)
        {
            input = "";
        }

        java.sql.Connection dbHandle = null;
        PreparedStatement queryExecutor = null;

        try
        {
            dbHandle = IO.getDBConnection();

            String sqlTemplate = "DELETE FROM users WHERE name=?";
            queryExecutor = dbHandle.prepareStatement(sqlTemplate);
            queryExecutor.setString(1, input);

            queryExecutor.execute();
        }
        catch (SQLException sqlEx)
        {
            IO.logger.log(Level.WARNING, "Database operation failed", sqlEx);
        }
        finally
        {
            try
            {
                if (queryExecutor != null)
                {
                    queryExecutor.close();
                }
            }
            catch (SQLException sqlEx)
            {
                IO.logger.log(Level.WARNING, "Statement close failure", sqlEx);
            }

            try
            {
                if (dbHandle != null)
                {
                    dbHandle.close();
                }
            }
            catch (SQLException sqlEx)
            {
                IO.logger.log(Level.WARNING, "Connection close failure", sqlEx);
            }
        }
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws Throwable, IOException
    {
        doPost(request, response);
    }
}