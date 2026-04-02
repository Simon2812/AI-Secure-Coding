package org.securitylab.suitecode;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/SuiteCase00032")
public class SuiteCase00032 extends HttpServlet {

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

        java.util.Map<String, String[]> requestMap = request.getParameterMap();
        String credentialInput = "";
        if (!requestMap.isEmpty()) {
            String[] entries = requestMap.get("SuiteCase00032");
            if (entries != null) credentialInput = entries[0];
        }

        try {
            String sql = "SELECT * from USERS where USERNAME='foo' and PASSWORD='" + credentialInput + "'";

            org.securitylab.suitecode.helpers.DatabaseHelper.JDBCtemplate.execute(sql);
            response.getWriter()
                    .println(
                            "No results can be displayed for query: "
                                    + org.securitylab.esapi.ESAPI.encoder().encodeForHTML(sql)
                                    + "<br>"
                                    + " because the Spring execute method doesn't return results.");

        } catch (org.springframework.dao.DataAccessException e) {
            if (org.securitylab.suitecode.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}