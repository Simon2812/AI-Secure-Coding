package org.cobaltgrid.verification;

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
        javax.servlet.http.Cookie issuedCookie =
                new javax.servlet.http.Cookie("UserLoginServlet", "bar");
        issuedCookie.setMaxAge(60 * 3);
        issuedCookie.setSecure(true);
        issuedCookie.setHttpOnly(true);
        issuedCookie.setPath(request.getRequestURI());
        issuedCookie.setDomain(new java.net.URL(request.getRequestURL().toString()).getHost());
        response.addCookie(issuedCookie);
        javax.servlet.RequestDispatcher rd =
                request.getRequestDispatcher("/sqli-00/UserLoginServlet.html");
        rd.include(request, response);
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");

        javax.servlet.http.Cookie[] cookieArray = request.getCookies();

        String cookieInput = "noCookieValueSupplied";
        if (cookieArray != null) {
            for (javax.servlet.http.Cookie currentCookie : cookieArray) {
                if (currentCookie.getName().equals("UserLoginServlet")) {
                    cookieInput = java.net.URLDecoder.decode(currentCookie.getValue(), "UTF-8");
                    break;
                }
            }
        }

        String resolvedCredential;
        String seedValue = "ABC";
        char branchIndicator = seedValue.charAt(2);

        switch (branchIndicator) {
            case 'A':
                resolvedCredential = cookieInput;
                break;
            case 'B':
                resolvedCredential = "static_value";
                break;
            case 'C':
            case 'D':
                resolvedCredential = cookieInput;
                break;
            default:
                resolvedCredential = "static_value";
                break;
        }

        String sql = "SELECT * from USERS where USERNAME='foo' and PASSWORD='" + resolvedCredential + "'";

        try {
            java.sql.Statement statement =
                    org.cobaltgrid.verification.helpers.DatabaseHelper.getSqlStatement();
            statement.execute(sql, new int[] {1, 2});
            org.cobaltgrid.verification.helpers.DatabaseHelper.printResults(statement, sql, response);
        } catch (java.sql.SQLException e) {
            if (org.cobaltgrid.verification.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}