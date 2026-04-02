package org.ironvault.scenario;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/UserLoginServlet")
public class UserLoginServlet extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");

        String headerInput = "";
        if (request.getHeader("UserLoginServlet") != null) {
            headerInput = request.getHeader("UserLoginServlet");
        }

        headerInput = java.net.URLDecoder.decode(headerInput, "UTF-8");

        String computed;
        String seed = "ABC";
        char branch = seed.charAt(2);

        switch (branch) {
            case 'A':
                computed = headerInput;
                break;
            case 'B':
                computed = "static_value";
                break;
            case 'C':
            case 'D':
                computed = headerInput;
                break;
            default:
                computed = "static_value";
                break;
        }

        String sql = "SELECT * from USERS where USERNAME=? and PASSWORD='" + computed + "'";

        try {
            java.sql.Connection connection =
                    org.ironvault.scenario.helpers.DatabaseHelper.getSqlConnection();
            java.sql.PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, "foo");
            statement.execute();
            org.ironvault.scenario.helpers.DatabaseHelper.printResults(statement, sql, response);
        } catch (java.sql.SQLException e) {
            if (org.ironvault.scenario.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}