package com.web.actions;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/actions/run")
public class ActionServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setContentType("text/plain;charset=UTF-8");

        String input = req.getParameter("item");
        if (input == null) input = "";

        String val = new Mapper().map(req, input);

        String cmd = "";
        String os = System.getProperty("os.name");

        if (os != null && os.indexOf("Windows") != -1) {
            cmd = "echo ";
        }

        Runtime runtime = Runtime.getRuntime();

        try {
            Process p = runtime.exec(cmd + val);
            resp.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }

    private class Mapper {

        public String map(HttpServletRequest req, String data)
                throws ServletException, IOException {

            String result = "";

            if (data != null) {
                java.util.List<String> buffer = new java.util.ArrayList<>();

                buffer.add("safe");
                buffer.add(data);
                buffer.add("extra");

                buffer.remove(0);

                result = buffer.get(0);
            }

            return result;
        }
    }
}