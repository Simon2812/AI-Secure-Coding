package com.store.jobs;

import java.io.IOException;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/jobs/execute")
public class JobExecutorServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setContentType("text/plain;charset=UTF-8");

        Map<String, String[]> parameters = req.getParameterMap();
        String input = "";

        if (!parameters.isEmpty()) {
            String[] arr = parameters.get("task");
            if (arr != null) {
                input = arr[0];
            }
        }

        String value = new Switcher().pick(req, input);

        String command = "";
        String os = System.getProperty("os.name");

        if (os != null && os.indexOf("Windows") != -1) {
            command = "echo ";
        }

        Runtime runtime = Runtime.getRuntime();

        try {
            Process p = runtime.exec(command + value);
            resp.getWriter().println("done");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }

    private class Switcher {

        public String pick(HttpServletRequest req, String data)
                throws ServletException, IOException {

            String result;
            String seed = "ABC";
            char selector = seed.charAt(2);

            switch (selector) {
                case 'A':
                    result = data;
                    break;
                case 'B':
                    result = "constant";
                    break;
                case 'C':
                case 'D':
                    result = data;
                    break;
                default:
                    result = "constant";
                    break;
            }

            return result;
        }
    }
}
