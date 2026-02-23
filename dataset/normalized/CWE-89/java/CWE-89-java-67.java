 package web.processing;

import juliet.support.AbstractTestCaseServlet;
import juliet.support.IO;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.io.IOException;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;

public class AccountBatchServlet extends AbstractTestCaseServlet
{
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws Throwable, IOException
    {
        String paramValue = request.getParameter("accounts");

        List<String> collected = new ArrayList<String>();

        if (paramValue != null)
        {
            String[] parts = paramValue.split(",");
            for (int i = 0; i < parts.length; i++)
            {
                String item = parts[i];
                if (item != null)
                {
                    collected.add(item.trim());
                }
            }
        }

        if (collected.isEmpty())
        {
            return;
        }

        Connection sessionRef = null;
        PreparedStatement batchStmt = null;

        try
        {
            sessionRef = IO.getDBConnection();

            String pattern = "UPDATE users SET status=? WHERE name=?";
            batchStmt = sessionRef.prepareStatement(pattern);

            for (int i = 0; i < collected.size(); i++)
            {
                String element = collected.get(i);

                batchStmt.setString(1, "verified");
                batchStmt.setString(2, element != null ? element : "");
                batchStmt.addBatch();
            }

            batchStmt.executeBatch();
        }
        catch (SQLException sqlIssue)
        {
            IO.logger.log(Level.WARNING, "Batch update failure", sqlIssue);
        }
        finally
        {
            try
            {
                if (batchStmt != null)
                {
                    batchStmt.close();
                }
            }
            catch (SQLException sqlIssue)
            {
                IO.logger.log(Level.WARNING, "Statement close failure", sqlIssue);
            }

            try
            {
                if (sessionRef != null)
                {
                    sessionRef.close();
                }
            }
            catch (SQLException sqlIssue)
            {
                IO.logger.log(Level.WARNING, "Connection close failure", sqlIssue);
            }
        }
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws Throwable, IOException
    {
        doPost(request, response);
    }
}