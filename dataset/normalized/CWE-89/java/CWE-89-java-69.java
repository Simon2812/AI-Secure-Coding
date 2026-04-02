package web.actions;

import juliet.support.AbstractTestCaseServlet;
import juliet.support.IO;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.io.IOException;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.util.logging.Level;

public class QueryActionServlet extends AbstractTestCaseServlet
{
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws Throwable, IOException
    {
        String rawQuery = request.getQueryString();
        String extracted = "";

        if (rawQuery != null)
        {
            String prefix = "id=";
            int index = rawQuery.indexOf(prefix);
            if (index >= 0)
            {
                extracted = rawQuery.substring(index + prefix.length());
            }
        }

        if (extracted == null)
        {
            extracted = "";
        }

        Connection channel = null;
        PreparedStatement executor = null;

        try
        {
            channel = IO.getDBConnection();

            String statementPattern = "DELETE FROM users WHERE name=?";
            executor = channel.prepareStatement(statementPattern);
            executor.setString(1, extracted);

            executor.execute();
        }
        catch (SQLException failure)
        {
            IO.logger.log(Level.WARNING, "Execution failure", failure);
        }
        finally
        {
            try
            {
                if (executor != null)
                {
                    executor.close();
                }
            }
            catch (SQLException failure)
            {
                IO.logger.log(Level.WARNING, "Statement close failure", failure);
            }

            try
            {
                if (channel != null)
                {
                    channel.close();
                }
            }
            catch (SQLException failure)
            {
                IO.logger.log(Level.WARNING, "Connection close failure", failure);
            }
        }
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws Throwable, IOException
    {
        doPost(request, response);
    }
}