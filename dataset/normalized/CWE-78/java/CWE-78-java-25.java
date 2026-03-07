package com.tools.monitor;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/monitor/run")
public class MonitorServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");

        Cookie c = new Cookie("sessionToken", "node1");
        c.setMaxAge(180);
        c.setSecure(true);
        c.setHttpOnly(true);
        c.setPath(request.getRequestURI());
        c.setDomain(new java.net.URL(request.getRequestURL().toString()).getHost());

        response.addCookie(c);

        RequestDispatcher rd = request.getRequestDispatcher("/monitor/run.html");
        rd.include(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        Cookie[] cookies = request.getCookies();

        String token = "none";
        if (cookies != null) {
            for (Cookie ck : cookies) {
                if ("sessionToken".equals(ck.getName())) {
                    token = URLDecoder.decode(ck.getValue(), StandardCharsets.UTF_8.name());
                    break;
                }
            }
        }

        String value = token;

        String command = "ping";
        String[] cmdArgs = {command, value};
        String[] envVars = {value};

        Runtime runtime = Runtime.getRuntime();

        try {
            Process process = runtime.exec(cmdArgs, envVars);
            response.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }
}