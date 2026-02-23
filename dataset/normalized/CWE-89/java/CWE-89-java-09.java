package web.actions;

import juliet.support.IO;
import juliet.support.AbstractTestCaseServlet;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.SQLException;

import java.util.logging.Level;

public class AccountStatusServlet extends AbstractTestCaseServlet {

    public void doPost(HttpServletRequest request, HttpServletResponse response) throws Throwable {

        String accountId = request.getParameter("account");

        Connection conn = null;
        Statement stmt = null;

        try {
            conn = IO.getDBConnection();
            stmt = conn.createStatement();

            stmt.executeUpdate("update accounts set status='closed' where id='" + accountId + "'");

            response.getWriter().println("Update completed.");

        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Update error", e);
        } catch (Exception e) {
            IO.logger.log(Level.WARNING, "Response error", e);
        } finally {

            try {
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Statement close error", e);
            }

            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Connection close error", e);
            }
        }
    }
}