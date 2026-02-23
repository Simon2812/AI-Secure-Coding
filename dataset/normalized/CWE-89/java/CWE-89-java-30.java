package org.redfort.assessment;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/UserSeedServlet")
public class UserSeedServlet extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        javax.servlet.http.Cookie issuedCookie =
                new javax.servlet.http.Cookie("UserSeedServlet", "bar");
        issuedCookie.setMaxAge(60 * 3);
        issuedCookie.setSecure(true);
        issuedCookie.setHttpOnly(true);
        issuedCookie.setPath(request.getRequestURI());
        issuedCookie.setDomain(new java.net.URL(request.getRequestURL().toString()).getHost());
        response.addCookie(issuedCookie);
        javax.servlet.RequestDispatcher rd =
                request.getRequestDispatcher("/sqli-00/UserSeedServlet.html");
        rd.include(request, response);
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");

        javax.servlet.http.Cookie[] cookieJar = request.getCookies();

        String cookieContent = "noCookieValueSupplied";
        if (cookieJar != null) {
            for (javax.servlet.http.Cookie current : cookieJar) {
                if (current.getName().equals("UserSeedServlet")) {
                    cookieContent = java.net.URLDecoder.decode(current.getValue(), "UTF-8");
                    break;
                }
            }
        }

        String extractedValue = "";
        if (cookieContent != null) {
            java.util.List<String> buffer = new java.util.ArrayList<String>();
            buffer.add("safe");
            buffer.add(cookieContent);
            buffer.add("moresafe");

            buffer.remove(0);

            extractedValue = buffer.get(0);
        }

        String sql = "INSERT INTO users (username, password) VALUES ('foo','" + extractedValue + "')";

        try {
            java.sql.Statement statement =
                    org.redfort.assessment.helpers.DatabaseHelper.getSqlStatement();
            int count = statement.executeUpdate(sql);
            org.redfort.assessment.helpers.DatabaseHelper.outputUpdateComplete(sql, response);
        } catch (java.sql.SQLException e) {
            if (org.redfort.assessment.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}