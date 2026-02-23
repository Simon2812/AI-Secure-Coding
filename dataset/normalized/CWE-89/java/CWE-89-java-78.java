package org.cybershield.web;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/EntryPoint078")
public class EntryPoint078 extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");

        javax.servlet.http.Cookie userCookie =
                new javax.servlet.http.Cookie("EntryPoint078", "bar");
        userCookie.setMaxAge(60 * 3);
        userCookie.setSecure(true);
        userCookie.setHttpOnly(true);
        userCookie.setPath(request.getRequestURI());
        userCookie.setDomain(new java.net.URL(request.getRequestURL().toString()).getHost());
        response.addCookie(userCookie);

        javax.servlet.RequestDispatcher rd =
                request.getRequestDispatcher("/sqli-00/EntryPoint078.html");
        rd.include(request, response);
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");

        javax.servlet.http.Cookie[] cookieJar = request.getCookies();

        String param = "noCookieValueSupplied";
        if (cookieJar != null) {
            for (javax.servlet.http.Cookie c : cookieJar) {
                if ("EntryPoint078".equals(c.getName())) {
                    param = java.net.URLDecoder.decode(c.getValue(), "UTF-8");
                    break;
                }
            }
        }

        String bar = "safe!";
        java.util.HashMap<String, Object> mapRef = new java.util.HashMap<String, Object>();
        mapRef.put("k1-078", "a_Value");
        mapRef.put("k2-078", param);
        mapRef.put("k3", "another_Value");
        bar = (String) mapRef.get("k2-078");
        bar = (String) mapRef.get("k1-078");

        String sql = "INSERT INTO users (username, password) VALUES ('foo','" + bar + "')";

        try {
            java.sql.Statement stmtUnit =
                    org.cybershield.helpers.DatabaseHelper.getSqlStatement();
            int count = stmtUnit.executeUpdate(sql);
            org.cybershield.helpers.DatabaseHelper.outputUpdateComplete(sql, response);
        } catch (java.sql.SQLException e) {
            if (org.cybershield.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}