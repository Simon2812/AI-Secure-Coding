package org.steelgate.reviewcode;

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
        doPost(request, response);
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");

        String headerInput = "";
        if (request.getHeader("UserLoginServlet") != null) {
            headerInput = request.getHeader("UserLoginServlet");
        }

        headerInput = java.net.URLDecoder.decode(headerInput, "UTF-8");

        org.steelgate.reviewcode.helpers.ThingInterface processor =
                org.steelgate.reviewcode.helpers.ThingFactory.createThing();
        String transformed = processor.doSomething(headerInput);

        String sql = "SELECT userid from USERS where USERNAME='foo' and PASSWORD='" + transformed + "'";

        try {
            Integer results =
                    org.steelgate.reviewcode.helpers.DatabaseHelper.JDBCtemplate.queryForObject(
                            sql, Integer.class);
            response.getWriter().println("Your results are: " + results);

        } catch (org.springframework.dao.EmptyResultDataAccessException e) {
            response.getWriter()
                    .println(
                            "No results returned for query: "
                                    + org.steelgate.esapi.ESAPI.encoder().encodeForHTML(sql));
        } catch (org.springframework.dao.DataAccessException e) {
            if (org.steelgate.reviewcode.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}