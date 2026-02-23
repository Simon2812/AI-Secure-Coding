package web.actions;

import juliet.support.IO;
import juliet.support.AbstractTestCaseServlet;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.SQLException;

import java.util.logging.Level;

public class OrderSearchServlet extends AbstractTestCaseServlet {

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws Throwable {

        String queryParam = request.getParameter("id");

        Connection connection = null;
        Statement statement = null;
        ResultSet result = null;

        try {
            connection = IO.getDBConnection();
            statement = connection.createStatement();

            result = statement.executeQuery("select * from orders where id='" + queryParam + "'");

            int count = 0;
            while (result.next()) {
                count++;
            }

            response.getWriter().println("Found " + count + " result(s).");

        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Database query error", e);
        } catch (Exception e) {
            IO.logger.log(Level.WARNING, "Response error", e);
        } finally {

            try {
                if (result != null) result.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "ResultSet close error", e);
            }

            try {
                if (statement != null) statement.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Statement close error", e);
            }

            try {
                if (connection != null) connection.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Connection close error", e);
            }
        }
    }
}