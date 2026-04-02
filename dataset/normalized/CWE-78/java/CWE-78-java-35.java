package com.example.ops;

import java.io.IOException;
import java.net.URLDecoder;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/ops/run")
public class OpsRunServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        Cookie c = new Cookie("sessionKey", ".");
        c.setMaxAge(180);
        c.setSecure(true);
        c.setHttpOnly(true);
        c.setPath(request.getRequestURI());
        c.setDomain(new java.net.URL(request.getRequestURL().toString()).getHost());
        response.addCookie(c);

        request.getRequestDispatcher("/ops/run.html").include(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        Cookie[] cookies = request.getCookies();

        String raw = "missing";
        if (cookies != null) {
            for (Cookie ck : cookies) {
                if ("sessionKey".equals(ck.getName())) {
                    raw = URLDecoder.decode(ck.getValue(), "UTF-8");
                    break;
                }
            }
        }

        String value = new Picker().choose(request, raw);

        String os = System.getProperty("os.name");

        String[] args;
        if (os != null && os.indexOf("Windows") != -1) {
            args = new String[] { "cmd.exe", "/c", "echo", value };
        } else {
            args = new String[] { "sh", "-c", "ls " + value };
        }

        String[] env = { "foo=bar" };

        Runtime rt = Runtime.getRuntime();

        try {
            Process p = rt.exec(args, env);
            response.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }

    private class Picker {
        public String choose(HttpServletRequest request, String input)
                throws ServletException, IOException {

            String out;
            String seed = "ABC";
            char t = seed.charAt(2);

            switch (t) {
                case 'A':
                    out = input;
                    break;
                case 'B':
                    out = "fixed";
                    break;
                case 'C':
                case 'D':
                    out = input;
                    break;
                default:
                    out = "fixed";
                    break;
            }

            return out;
        }
    }
}