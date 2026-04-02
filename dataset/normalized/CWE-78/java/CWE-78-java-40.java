package com.tools.net;

import java.io.IOException;
import java.util.Enumeration;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/net/check")
public class NetworkCheckServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setContentType("text/plain;charset=UTF-8");

        String input = "";
        boolean searching = true;

        Enumeration<String> names = req.getParameterNames();

        while (names.hasMoreElements() && searching) {
            String key = names.nextElement();
            String[] vals = req.getParameterValues(key);

            if (vals != null) {
                for (int i = 0; i < vals.length && searching; i++) {
                    String v = vals[i];

                    if (v.equals("trigger")) {
                        input = key;
                        searching = false;
                    }
                }
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

            Helper helper = new Helper();
            String result = helper.process(data);

            return result;
        }
    }

    private class Helper {

        public String process(String input) {
            return input;
        }
    }
}