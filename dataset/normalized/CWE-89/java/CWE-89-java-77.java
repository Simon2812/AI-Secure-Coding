package org.fortifyzone.web;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-00/EntryPoint771")
public class EntryPoint771 extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");

        javax.servlet.http.Cookie sessionCookie =
                new javax.servlet.http.Cookie("EntryPoint771", "bar");
        sessionCookie.setMaxAge(60 * 3);
        sessionCookie.setSecure(true);
        sessionCookie.setHttpOnly(true);
        sessionCookie.setPath(request.getRequestURI());
        sessionCookie.setDomain(
                new java.net.URL(request.getRequestURL().toString()).getHost());
        response.addCookie(sessionCookie);

        javax.servlet.RequestDispatcher dispatcher =
                request.getRequestDispatcher("/sqli-00/EntryPoint771.html");
        dispatcher.include(request, response);
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");

        javax.servlet.http.Cookie[] cookies = request.getCookies();

        String input = "noCookieValueSupplied";
        if (cookies != null) {
            for (javax.servlet.http.Cookie c : cookies) {
                if ("EntryPoint771".equals(c.getName())) {
                    input = java.net.URLDecoder.decode(c.getValue(), "UTF-8");
                    break;
                }
            }
        }

        String value;

        int pivot = 86;
        if ((7 * 42) - pivot > 200)
            value = "staticValue";
        else
            value = input;

        try {
            String sql =
                    "SELECT * from USERS where USERNAME='foo' and PASSWORD='"
                            + value
                            + "'";

            org.fortifyzone.helpers.DatabaseHelper.JDBCtemplate.batchUpdate(sql);

            response.getWriter()
                    .println(
                            "No results can be displayed for query: "
                                    + org.fortifyzone.esapi.ESAPI.encoder()
                                            .encodeForHTML(sql)
                                    + "<br>"
                                    + " because batchUpdate does not return results.");
        } catch (org.springframework.dao.DataAccessException e) {
            if (org.fortifyzone.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}