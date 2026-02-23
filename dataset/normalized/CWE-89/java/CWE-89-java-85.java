package org.cybershield.web;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/ParamBridge430")
public class ParamBridge430 extends HttpServlet {

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

        String param = request.getParameter("ParamBridge430");
        if (param == null) param = "";

        String bar;

        int num = 106;
        bar = (7 * 18) + num > 200 ? "This_should_always_happen" : param;

        String sql = "SELECT * from USERS where USERNAME=? and PASSWORD=?";

        try {
            java.sql.Connection dbConn =
                    org.cybershield.helpers.DatabaseHelper.getSqlConnection();

            java.sql.PreparedStatement ps =
                    dbConn.prepareStatement(
                            sql,
                            java.sql.ResultSet.TYPE_FORWARD_ONLY,
                            java.sql.ResultSet.CONCUR_READ_ONLY,
                            java.sql.ResultSet.CLOSE_CURSORS_AT_COMMIT);

            ps.setString(1, "foo");
            ps.setString(2, bar);

            ps.execute();
            org.cybershield.helpers.DatabaseHelper.printResults(ps, sql, response);
        } catch (java.sql.SQLException e) {
            if (org.cybershield.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}