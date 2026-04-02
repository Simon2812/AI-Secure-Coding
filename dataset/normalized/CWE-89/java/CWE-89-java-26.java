package org.guardianlab.safecode;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/Case00043")
public class Case00043 extends HttpServlet {

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

        org.guardianlab.safecode.helpers.RequestWrapper wrapper =
                new org.guardianlab.safecode.helpers.RequestWrapper(request);
        String inputValue = wrapper.getValue("Case00043");
        if (inputValue == null) inputValue = "";

        String sql = "INSERT INTO users (username, password) VALUES ('foo','" + inputValue + "')";

        try {
            java.sql.Statement statement =
                    org.guardianlab.safecode.helpers.DatabaseHelper.getSqlStatement();
            int count = statement.executeUpdate(sql, new int[] {1, 2});
            org.guardianlab.safecode.helpers.DatabaseHelper.outputUpdateComplete(sql, response);
        } catch (java.sql.SQLException e) {
            if (org.guardianlab.safecode.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}