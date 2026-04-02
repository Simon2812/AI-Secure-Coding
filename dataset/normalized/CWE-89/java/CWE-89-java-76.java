package org.trustwave.sea;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/bob")
public class BenchmarkTest00645 extends HttpServlet {

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

        org.trustwave.helpers.RequestWrapper reqWrap =
                new org.trustwave.helpers.RequestWrapper(request);
        String token = reqWrap.getTheValue("bob");
        if (token == null) token = "";

        String callSql = "{call ?}";

        try {
            java.sql.Connection dbConn =
                    org.trustwave.helpers.DatabaseHelper.getSqlConnection();
            java.sql.CallableStatement cs =
                    dbConn.prepareCall(
                            callSql,
                            java.sql.ResultSet.TYPE_FORWARD_ONLY,
                            java.sql.ResultSet.CONCUR_READ_ONLY,
                            java.sql.ResultSet.CLOSE_CURSORS_AT_COMMIT);

            cs.setString(1, token);

            java.sql.ResultSet rs = cs.executeQuery();
            org.trustwave.helpers.DatabaseHelper.printResults(rs, callSql, response);
        } catch (java.sql.SQLException e) {
            if (org.trustwave.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}