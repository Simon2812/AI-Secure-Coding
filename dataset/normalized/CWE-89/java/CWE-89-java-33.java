package org.silverline.auditcase;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/UserSeedServlet")
public class UserSeedServlet extends HttpServlet {

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

        String headerValue = "";
        if (request.getHeader("UserSeedServlet") != null) {
            headerValue = request.getHeader("UserSeedServlet");
        }

        headerValue = java.net.URLDecoder.decode(headerValue, "UTF-8");

        String computedValue;

        int reference = 106;
        computedValue = (7 * 42) - reference > 200 ? "This should never happen" : headerValue;

        String sql = "INSERT INTO users (username, password) VALUES ('foo','" + computedValue + "')";

        try {
            java.sql.Statement statement =
                    org.silverline.auditcase.helpers.DatabaseHelper.getSqlStatement();
            int count = statement.executeUpdate(sql, new String[] {"USERNAME", "PASSWORD"});
            org.silverline.auditcase.helpers.DatabaseHelper.outputUpdateComplete(sql, response);
        } catch (java.sql.SQLException e) {
            if (org.silverline.auditcase.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}