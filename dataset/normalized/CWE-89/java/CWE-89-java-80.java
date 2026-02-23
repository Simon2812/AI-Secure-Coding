package org.securecore.web;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/Entry")
public class EntryPoint080 extends HttpServlet {

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

        String headerText = "";
        String raw = request.getHeader("Entry");
        if (raw != null) {
            headerText = raw;
        }

        headerText = java.net.URLDecoder.decode(headerText, "UTF-8");

        String chosen = "alsosafe";
        if (headerText != null) {
            java.util.List<String> values = new java.util.ArrayList<String>();
            values.add("safe");
            values.add(headerText);
            values.add("moresafe");

            values.remove(0);

            chosen = values.get(1);
        }

        try {
            String sql = "SELECT * from USERS where USERNAME='foo' and PASSWORD='" + chosen + "'";

            org.securecore.helpers.DatabaseHelper.JDBCtemplate.batchUpdate(sql);
            response.getWriter()
                    .println(
                            "No results can be displayed for query: "
                                    + org.securecore.esapi.ESAPI.encoder().encodeForHTML(sql)
                                    + "<br>"
                                    + " because the Spring batchUpdate method doesn't return results.");
        } catch (org.springframework.dao.DataAccessException e) {
            if (org.securecore.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}