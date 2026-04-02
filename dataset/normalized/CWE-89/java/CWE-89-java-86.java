package org.cybermatrix.web;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/ParamMesh440")
public class ParamMesh440 extends HttpServlet {

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

        String param = request.getParameter("ParamMesh440");
        if (param == null) param = "";

        String bar = "safe!";
        java.util.HashMap<String, Object> mapRef = new java.util.HashMap<String, Object>();
        mapRef.put("kA-440", "a_Value");
        mapRef.put("kB-440", param);
        mapRef.put("kC", "another_Value");
        bar = (String) mapRef.get("kB-440");
        bar = (String) mapRef.get("kA-440");

        String sql = "INSERT INTO users (username, password) VALUES (?, ?)";

        java.sql.Connection dbConn = null;
        java.sql.PreparedStatement ps = null;

        try {
            dbConn = org.cybermatrix.helpers.DatabaseHelper.getSqlConnection();
            ps = dbConn.prepareStatement(sql, java.sql.Statement.RETURN_GENERATED_KEYS);

            ps.setString(1, "foo");
            ps.setString(2, bar);

            ps.executeUpdate();
            org.cybermatrix.helpers.DatabaseHelper.outputUpdateComplete(sql, response);
        } catch (java.sql.SQLException e) {
            if (org.cybermatrix.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        } finally {
            try { if (ps != null) ps.close(); } catch (java.sql.SQLException ignored) { }
            try { if (dbConn != null) dbConn.close(); } catch (java.sql.SQLException ignored) { }
        }
    }
}