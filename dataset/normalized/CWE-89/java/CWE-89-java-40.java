package org.sentinelgrid.testcode;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-01/ProcedureExecutorServlet")
public class ProcedureExecutorServlet extends HttpServlet {

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

        String param = "";
        boolean flag = true;
        java.util.Enumeration<String> names = request.getParameterNames();
        while (names.hasMoreElements() && flag) {
            String name = (String) names.nextElement();
            String[] values = request.getParameterValues(name);
            if (values != null) {
                for (int i = 0; i < values.length && flag; i++) {
                    String value = values[i];
                    if (value.equals("ProcedureExecutorServlet")) {
                        param = name;
                        flag = false;
                    }
                }
            }
        }

        String bar;

        int num = 196;
        if ((500 / 42) + num > 200) bar = param;
        else bar = "This should never happen";

        String sql = "{call " + bar + "}";

        try {
            java.sql.Connection connection =
                    org.sentinelgrid.helpers.DatabaseHelper.getSqlConnection();
            java.sql.CallableStatement statement =
                    connection.prepareCall(
                            sql,
                            java.sql.ResultSet.TYPE_FORWARD_ONLY,
                            java.sql.ResultSet.CONCUR_READ_ONLY,
                            java.sql.ResultSet.CLOSE_CURSORS_AT_COMMIT);
            java.sql.ResultSet rs = statement.executeQuery();
            org.sentinelgrid.helpers.DatabaseHelper.printResults(rs, sql, response);
        } catch (java.sql.SQLException e) {
            if (org.sentinelgrid.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}