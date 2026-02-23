package web.endpoint;

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

public class ProfileStatusServlet extends AbstractTestCaseServlet
{
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws Throwable, IOException
    {
        String extracted = "";

        Cookie[] cookies = request.getCookies();
        if (cookies != null)
        {
            for (int i = 0; i < cookies.length; i++)
            {
                Cookie current = cookies[i];
                if ("UserToken".equals(current.getName()))
                {
                    extracted = current.getValue();
                    break;
                }
            }
        }

        if (extracted == null)
        {
            extracted = "";
        }

        Connection sqlSession = null;
        PreparedStatement updateCmd = null;

        try
        {
            sqlSession = IO.getDBConnection();

            String queryPattern = "UPDATE users SET status=? WHERE name=?";
            updateCmd = sqlSession.prepareStatement(queryPattern);

            updateCmd.setString(1, "active");
            updateCmd.setString(2, extracted);

            updateCmd.executeUpdate();
        }
        catch (SQLException error)
        {
            IO.logger.log(Level.WARNING, "Update failed", error);
        }
        finally
        {
            try
            {
                if (updateCmd != null)
                {
                    updateCmd.close();
                }
            }
            catch (SQLException error)
            {
                IO.logger.log(Level.WARNING, "Statement close failure", error);
            }

            try
            {
                if (sqlSession != null)
                {
                    sqlSession.close();
                }
            }
            catch (SQLException error)
            {
                IO.logger.log(Level.WARNING, "Connection close failure", error);
            }
        }
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws Throwable, IOException
    {
        doPost(request, response);
    }
}