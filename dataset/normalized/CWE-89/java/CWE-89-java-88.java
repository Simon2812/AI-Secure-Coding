package org.trustwave.web;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-01/FieldMixer519")
public class FieldMixer extends HttpServlet {

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

        java.util.Map<String, String[]> map = request.getParameterMap();
        String param = "";
        if (!map.isEmpty()) {
            String[] values = map.get("FieldMixer");
            if (values != null) param = values[0];
        }

        String bar = "safe!";
        java.util.HashMap<String, Object> stage = new java.util.HashMap<String, Object>();
        stage.put("kA-519", "a_Value");
        stage.put("kB-519", param);
        stage.put("kC", "another_Value");
        bar = (String) stage.get("kB-519");
        bar = (String) stage.get("kA-519");

        String sql = "INSERT INTO users (username, password) VALUES (?, ?)";

        try {
            java.sql.Connection c =
                    org.trustwave.helpers.DatabaseHelper.getSqlConnection();
            java.sql.PreparedStatement ps =
                    c.prepareStatement(sql, new String[] {"USERNAME", "PASSWORD"});
            ps.setString(1, "foo");
            ps.setString(2, bar);

            int count = ps.executeUpdate();
            org.trustwave.helpers.DatabaseHelper.outputUpdateComplete(sql, response);
        } catch (java.sql.SQLException e) {
            if (org.trustwave.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}