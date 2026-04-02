package com.tools.net;

import java.io.IOException;
import java.util.Enumeration;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/net/scan")
public class NetworkScanServlet extends HttpServlet {

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
        String os = System.getProperty("os.name");

        if (os.indexOf("Windows") != -1) {
            cmd = org.owasp.benchmark.helpers.Utils.getOSCommandString("echo");
        }

        Runtime runtime = Runtime.getRuntime();

        try {
            Process p = runtime.exec(cmd + value);
            org.owasp.benchmark.helpers.Utils.printOSCommandResults(p, resp);
        } catch (IOException e) {
            System.out.println("Problem executing command");
            resp.getWriter().println(
                    org.owasp.esapi.ESAPI.encoder().encodeForHTML(e.getMessage()));
            return;
        }
    }

    private class Transformer {

        public String apply(HttpServletRequest req, String data)
                throws ServletException, IOException {

            String result = "";

            if (data != null) {
                result =
                        new String(
                                org.apache.commons.codec.binary.Base64.decodeBase64(
                                        org.apache.commons.codec.binary.Base64.encodeBase64(
                                                data.getBytes())));
            }

            return result;
        }
    }
}