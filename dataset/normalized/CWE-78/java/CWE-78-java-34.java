package com.example.exec;

import java.io.IOException;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/exec/run")
public class ExecRunServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        Cookie cookie =
                new Cookie("sessionToken", "ABC");
        cookie.setMaxAge(180);
        cookie.setSecure(true);
        cookie.setHttpOnly(true);
        cookie.setPath(request.getRequestURI());
        cookie.setDomain(new java.net.URL(request.getRequestURL().toString()).getHost());

        response.addCookie(cookie);

        request.getRequestDispatcher("/exec/page.html").include(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        Cookie[] cookies = request.getCookies();

        String input = "missing";
        if (cookies != null) {
            for (Cookie c : cookies) {
                if ("sessionToken".equals(c.getName())) {
                    input = URLDecoder.decode(c.getValue(), "UTF-8");
                    break;
                }
            }
        }

        String value = new Helper().transform(request, input);

        List<String> command = new ArrayList<>();

        String os = System.getProperty("os.name");

        if (os.indexOf("Windows") != -1) {
            command.add("cmd.exe");
            command.add("/c");
        } else {
            command.add("sh");
            command.add("-c");
        }

        command.add("date " + value);

        ProcessBuilder pb = new ProcessBuilder(command);

        try {
            Process p = pb.start();
            response.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }

    private class Helper {

        public String transform(HttpServletRequest request, String input)
                throws ServletException, IOException {

            String result = input;
            return result;
        }
    }
}