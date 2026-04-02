package com.service;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/service/run")
public class TaskServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");

        Cookie c = new Cookie("sessionLabel", "HELLO");
        c.setMaxAge(180);
        c.setSecure(true);
        c.setHttpOnly(true);
        c.setPath(request.getRequestURI());
        c.setDomain(new java.net.URL(request.getRequestURL().toString()).getHost());

        response.addCookie(c);

        RequestDispatcher rd = request.getRequestDispatcher("/service/run.html");
        rd.include(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        Cookie[] cookies = request.getCookies();

        String input = "none";
        if (cookies != null) {
            for (Cookie ck : cookies) {
                if ("sessionLabel".equals(ck.getName())) {
                    input = URLDecoder.decode(ck.getValue(), StandardCharsets.UTF_8.name());
                    break;
                }
            }
        }

        String value;
        String seed = "XYZ";
        char key = seed.charAt(2);

        switch (key) {
            case 'X':
                value = input;
                break;
            case 'Y':
                value = "default";
                break;
            case 'Z':
            case 'W':
                value = input;
                break;
            default:
                value = "default";
                break;
        }

        List<String> args = new ArrayList<>();

        String os = System.getProperty("os.name");
        if (os != null && os.contains("Windows")) {
            args.add("cmd.exe");
            args.add("/c");
        } else {
            args.add("sh");
            args.add("-c");
        }

        args.add("echo " + value);

        ProcessBuilder builder = new ProcessBuilder(args);

        try {
            Process p = builder.start();
            response.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }
}