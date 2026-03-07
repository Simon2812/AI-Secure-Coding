package com.tools.system;

import java.io.IOException;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/system/inspect")
public class NetworkInspectServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setContentType("text/plain;charset=UTF-8");

        Map<String, String[]> params = req.getParameterMap();
        String input = "";

        if (!params.isEmpty()) {
            String[] values = params.get("data");

            if (values != null) {
                input = values[0];
            }
        }

        String value = new Transformer().apply(req, input);

        String cmd = "";
        String a1 = "";
        String a2 = "";
        String[] args;

        String os = System.getProperty("os.name");

        if (os != null && os.indexOf("Windows") != -1) {
            a1 = "cmd.exe";
            a2 = "/c";
            cmd = "echo";
            args = new String[] {a1, a2, cmd, value};
        } else {
            a1 = "sh";
            a2 = "-c";
            cmd = "ping -c1 ";
            args = new String[] {a1, a2, cmd + value};
        }

        Runtime runtime = Runtime.getRuntime();

        try {
            Process p = runtime.exec(args);
            resp.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }

    private class Transformer {

        public String apply(HttpServletRequest req, String data)
                throws ServletException, IOException {

            String result = "constant";

            if (data != null) {
                java.util.List<String> list = new java.util.ArrayList<>();
                list.add("first");
                list.add(data);
                list.add("last");

                list.remove(0);

                result = list.get(1);
            }

            return result;
        }
    }
}