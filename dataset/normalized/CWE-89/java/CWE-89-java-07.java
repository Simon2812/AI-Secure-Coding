package web.handlers;

import juliet.support.IO;
import juliet.support.AbstractTestCaseServlet;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.SQLException;

import java.util.logging.Level;

public class CookieUserLookupServlet extends AbstractTestCaseServlet {

    public void doPost(HttpServletRequest request, HttpServletResponse response) throws Throwable {

        String userKey = "";
        Cookie[] cookies = request.getCookies();

        if (cookies != null) {
            for (int i = 0; i < cookies.length; i++) {
                Cookie c = cookies[i];
                if (c != null) {
                    userKey = c.getValue();
                    break;
                }
            }
        }

        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;

        try {
            conn = IO.getDBConnection();
            stmt = conn.createStatement();

            rs = stmt.executeQuery("select * from users where name='" + userKey + "'");

            IO.writeLine(rs.getRow());
        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Database error", e);
        } finally {

            try {
                if (rs != null) rs.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Error closing ResultSet", e);
            }

            try {
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Error closing Statement", e);
            }

            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Error closing Connection", e);
            }
        }
    }
}