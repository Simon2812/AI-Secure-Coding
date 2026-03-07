package com.example.tools;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Enumeration;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/ops/echo")
public class EchoServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        String value = "";
        Enumeration<String> headers = request.getHeaders("X-Label");

        if (headers != null && headers.hasMoreElements()) {
            value = headers.nextElement();
        }

        value = URLDecoder.decode(value, StandardCharsets.UTF_8.name());

        String command = "";
        String os = System.getProperty("os.name");

        if (os != null && os.contains("Windows")) {
            command = "cmd.exe /c echo ";
        } else {
            command = "sh -c echo ";
        }

        Runtime runtime = Runtime.getRuntime();

        try {
            Process process = runtime.exec(command + value);
            response.getWriter().println("done");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }
}