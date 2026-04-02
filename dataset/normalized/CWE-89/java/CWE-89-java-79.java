package org.lockbox.web;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/EntryPoint079")
public class EntryPoint extends HttpServlet {

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
        String candidate = request.getHeader("EntryPoint");
        if (candidate != null) {
            headerValue = candidate;
        }

        headerValue = java.net.URLDecoder.decode(headerValue, "UTF-8");

        String selected = "alsosafe";
        if (headerValue != null) {
            java.util.List<String> values = new java.util.ArrayList<String>();
            values.add("safe");
            values.add(headerValue);
            values.add("moresafe");

            values.remove(0);

            selected = values.get(1);
        }

        String sql = "{call " + selected + "}";

        try {
            java.sql.Connection dbConn =
                    org.lockbox.helpers.DatabaseHelper.getSqlConnection();
            java.sql.CallableStatement callStmt =
                    dbConn.prepareCall(
                            sql,
                            java.sql.ResultSet.TYPE_FORWARD_ONLY,
                            java.sql.ResultSet.CONCUR_READ_ONLY);
            java.sql.ResultSet rs = callStmt.executeQuery();
            org.lockbox.helpers.DatabaseHelper.printResults(rs, sql, response);
        } catch (java.sql.SQLException e) {
            if (org.lockbox.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}