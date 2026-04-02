package com.acme.processing;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/service/execute")
public class ServiceEntryPoint extends HttpServlet {

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

        String procedureName = "";
        if (request.getHeader("X-Procedure") != null) {
            procedureName = request.getHeader("X-Procedure");
        }

        procedureName = java.net.URLDecoder.decode(procedureName, "UTF-8");

        String callStatement = "{call " + procedureName + "}";

        try {
            java.sql.Connection connection =
                    com.acme.processing.DbConnector.getConnection();
            java.sql.CallableStatement callable = connection.prepareCall(callStatement);
            java.sql.ResultSet rs = callable.executeQuery();
            com.acme.processing.ResultPrinter.print(rs, callStatement, response);

        } catch (java.sql.SQLException e) {
            if (com.acme.processing.DbConnector.hideErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}