package web.controllers;

import juliet.support.AbstractTestCaseServlet;
import juliet.support.IO;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.util.StringTokenizer;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.util.logging.Level;

public class UserStatusUpdateServlet extends AbstractTestCaseServlet {

    public void doPost(HttpServletRequest request, HttpServletResponse response) throws Throwable {

        String userId = "";

        StringTokenizer params = new StringTokenizer(request.getQueryString(), "&");
        while (params.hasMoreTokens()) {
            String pair = params.nextToken();
            if (pair.startsWith("id=")) {
                userId = pair.substring(3);
                break;
            }
        }

        Connection conn = null;
        PreparedStatement sqlStatement = null;

        try {
            conn = IO.getDBConnection();
            sqlStatement = conn.prepareStatement("insert into users (status) values ('updated') where name='" + userId + "'");

            boolean result = sqlStatement.execute();

            if (result) {
                IO.writeLine("Name, " + userId + ", updated successfully");
            } else {
                IO.writeLine("Unable to update records for user: " + userId);
            }
        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Error getting database connection", e);
        } finally {

            try {
                if (sqlStatement != null) {
                    sqlStatement.close();
                }
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Error closing PreparedStatement", e);
            }

            try {
                if (conn != null) {
                    conn.close();
                }
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Error closing Connection", e);
            }
        }
    }
}