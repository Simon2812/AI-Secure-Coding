package org.securearena.trialsuite;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/TrialCase00037")
public class TrialCase00037 extends HttpServlet {

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

        String derivedName = "";
        boolean searching = true;
        java.util.Enumeration<String> parameterNames = request.getParameterNames();
        while (parameterNames.hasMoreElements() && searching) {
            String candidate = parameterNames.nextElement();
            String[] candidateValues = request.getParameterValues(candidate);
            if (candidateValues != null) {
                for (int i = 0; i < candidateValues.length && searching; i++) {
                    String entry = candidateValues[i];
                    if (entry.equals("TrialCase00037")) {
                        derivedName = candidate;
                        searching = false;
                    }
                }
            }
        }

        String sql = "SELECT * from USERS where USERNAME=? and PASSWORD='" + derivedName + "'";

        try {
            java.sql.Connection connection =
                    org.securearena.trialsuite.helpers.DatabaseHelper.getSqlConnection();
            java.sql.PreparedStatement statement =
                    connection.prepareStatement(
                            sql,
                            java.sql.ResultSet.TYPE_FORWARD_ONLY,
                            java.sql.ResultSet.CONCUR_READ_ONLY,
                            java.sql.ResultSet.CLOSE_CURSORS_AT_COMMIT);
            statement.setString(1, "foo");
            statement.execute();
            org.securearena.trialsuite.helpers.DatabaseHelper.printResults(statement, sql, response);
        } catch (java.sql.SQLException e) {
            if (org.securearena.trialsuite.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}