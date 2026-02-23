package org.defenselab.testbed;

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
        javax.servlet.http.Cookie userCookie =
                new javax.servlet.http.Cookie("UserLoginServlet", "bar");
        userCookie.setMaxAge(60 * 3);
        userCookie.setSecure(true);
        userCookie.setHttpOnly(true);
        userCookie.setPath(request.getRequestURI());
        userCookie.setDomain(new java.net.URL(request.getRequestURL().toString()).getHost());
        response.addCookie(userCookie);
        javax.servlet.RequestDispatcher rd =
                request.getRequestDispatcher("/sqli-00/UserLoginServlet.html");
        rd.include(request, response);
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");

        javax.servlet.http.Cookie[] cookies = request.getCookies();

        String cookieData = "noCookieValueSupplied";
        if (cookies != null) {
            for (javax.servlet.http.Cookie c : cookies) {
                if (c.getName().equals("UserLoginServlet")) {
                    cookieData = java.net.URLDecoder.decode(c.getValue(), "UTF-8");
                    break;
                }
            }
        }

        String extractedValue = "safe!";
        java.util.HashMap<String, Object> containerMap = new java.util.HashMap<String, Object>();
        containerMap.put("alphaKey", "a-Value");
        containerMap.put("betaKey", cookieData);
        containerMap.put("gammaKey", "another-Value");
        extractedValue = (String) containerMap.get("betaKey");

        String sql = "SELECT * from USERS where USERNAME=? and PASSWORD='" + extractedValue + "'";

        try {
            java.sql.Connection connection =
                    org.defenselab.testbed.helpers.DatabaseHelper.getSqlConnection();
            java.sql.PreparedStatement statement =
                    connection.prepareStatement(
                            sql,
                            java.sql.ResultSet.TYPE_FORWARD_ONLY,
                            java.sql.ResultSet.CONCUR_READ_ONLY,
                            java.sql.ResultSet.CLOSE_CURSORS_AT_COMMIT);
            statement.setString(1, "foo");
            statement.execute();
            org.defenselab.testbed.helpers.DatabaseHelper.printResults(statement, sql, response);
        } catch (java.sql.SQLException e) {
            if (org.defenselab.testbed.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}