package com.app.runner;

import java.io.IOException;
import java.net.URLDecoder;
import java.util.Enumeration;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/runner/task")
public class TaskServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setContentType("text/plain;charset=UTF-8");

        String headerValue = "";
        Enumeration<String> headerEnum = req.getHeaders("X-Task");

        if (headerEnum != null && headerEnum.hasMoreElements()) {
            headerValue = headerEnum.nextElement();
        }

        headerValue = URLDecoder.decode(headerValue, "UTF-8");

        String value = new Resolver().resolve(req, headerValue);

        String baseCommand = "whoami";
        String[] args = {baseCommand};
        String[] env = {value};

        Runtime runtime = Runtime.getRuntime();

        try {
            Process p = runtime.exec(args, env);
            resp.getWriter().println("done");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }

    private class Resolver {

        public String resolve(HttpServletRequest req, String input)
                throws ServletException, IOException {

            String result;

            int marker = 106;

            result = (7 * 42) - marker > 200 ? "unused" : input;

            return result;
        }
    }
}