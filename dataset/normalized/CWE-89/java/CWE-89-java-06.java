package web.handlers;

import juliet.support.IO;
import juliet.support.AbstractTestCaseServlet;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.SQLException;

import java.util.logging.Level;

public class AuditServlet extends AbstractTestCaseServlet {

    public void doPost(HttpServletRequest request, HttpServletResponse response) {

        String cookieValue = null;

        Cookie[] cookieArray = request.getCookies();
        if (cookieArray != null) {
            for (int i = 0; i < cookieArray.length; i++) {
                if ("user".equals(cookieArray[i].getName())) {
                    cookieValue = cookieArray[i].getValue();
                    break;
                }
            }
        }

        if (cookieValue != null) {

            String[] tokens = cookieValue.split(";");
            int affected = 0;

            Connection dbConn = null;
            Statement batchStmt = null;

            try {
                dbConn = IO.getDBConnection();
                batchStmt = dbConn.createStatement();

                for (int i = 0; i < tokens.length; i++) {
                    batchStmt.addBatch("update audit_log set reviewed=1 where actor='" + tokens[i] + "'");
                }

                int[] results = batchStmt.executeBatch();

                for (int i = 0; i < results.length; i++) {
                    if (results[i] > 0) {
                        affected++;
                    }
                }

                response.getWriter().println("Marked " + affected + " entries.");

            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Batch update error", e);
            } catch (Exception e) {
                IO.logger.log(Level.WARNING, "Response error", e);
            } finally {

                try {
                    if (batchStmt != null) batchStmt.close();
                } catch (SQLException e) {
                    IO.logger.log(Level.WARNING, "Statement close error", e);
                }

                try {
                    if (dbConn != null) dbConn.close();
                } catch (SQLException e) {
                    IO.logger.log(Level.WARNING, "Connection close error", e);
                }
            }
        }
    }
}