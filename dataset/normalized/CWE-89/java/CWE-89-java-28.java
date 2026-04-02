package org.shieldzone.casefiles;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/UserLoginServlet")
public class UserLoginServlet extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        javax.servlet.http.Cookie sessionCookie =
                new javax.servlet.http.Cookie("UserLoginServlet", "bar");
        sessionCookie.setMaxAge(60 * 3);
        sessionCookie.setSecure(true);
        sessionCookie.setHttpOnly(true);
        sessionCookie.setPath(request.getRequestURI());
        sessionCookie.setDomain(new java.net.URL(request.getRequestURL().toString()).getHost());
        response.addCookie(sessionCookie);
        javax.servlet.RequestDispatcher rd =
                request.getRequestDispatcher("/sqli-00/UserLoginServlet.html");
        rd.include(request, response);
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");

        javax.servlet.http.Cookie[] cookies = request.getCookies();

        String cookiePayload = "noCookieValueSupplied";
        if (cookies != null) {
            for (javax.servlet.http.Cookie c : cookies) {
                if (c.getName().equals("UserLoginServlet")) {
                    cookiePayload = java.net.URLDecoder.decode(c.getValue(), "UTF-8");
                    break;
                }
            }
        }

        String computedValue = "";
        if (cookiePayload != null) {
            java.util.List<String> tempList = new java.util.ArrayList<String>();
            tempList.add("safe");
            tempList.add(cookiePayload);
            tempList.add("moresafe");

            tempList.remove(0);

            computedValue = tempList.get(0);
        }

        String sql = "SELECT * from USERS where USERNAME='foo' and PASSWORD='" + computedValue + "'";

        try {
            java.sql.Statement statement =
                    org.shieldzone.casefiles.helpers.DatabaseHelper.getSqlStatement();
            statement.execute(sql, java.sql.Statement.RETURN_GENERATED_KEYS);
            org.shieldzone.casefiles.helpers.DatabaseHelper.printResults(statement, sql, response);
        } catch (java.sql.SQLException e) {
            if (org.shieldzone.casefiles.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}