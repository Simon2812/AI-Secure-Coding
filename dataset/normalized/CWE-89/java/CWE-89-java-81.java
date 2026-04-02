package org.safeguardlab.web;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/SignalRouter205")
public class SignalRouter205 extends HttpServlet {

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

        String rawHeader = "";
        String header = request.getHeader("SignalRouter205");
        if (header != null) {
            rawHeader = header;
        }

        rawHeader = java.net.URLDecoder.decode(rawHeader, "UTF-8");

        String picked = "alsosafe";
        if (rawHeader != null) {
            java.util.List<String> seq = new java.util.ArrayList<String>();
            seq.add("safe");
            seq.add(rawHeader);
            seq.add("moresafe");

            seq.remove(0);

            picked = seq.get(1);
        }

        String sql = "INSERT INTO users (username, password) VALUES ('foo','" + picked + "')";

        try {
            java.sql.Statement stmtHandle =
                    org.safeguardlab.helpers.DatabaseHelper.getSqlStatement();
            int count = stmtHandle.executeUpdate(sql, new String[] {"USERNAME", "PASSWORD"});
            org.safeguardlab.helpers.DatabaseHelper.outputUpdateComplete(sql, response);
        } catch (java.sql.SQLException e) {
            if (org.safeguardlab.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}