package com.app.ops;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Enumeration;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/ops/run")
public class OpsRunServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        String chosenName = "";
        boolean searching = true;

        Enumeration<String> names = request.getParameterNames();
        while (names.hasMoreElements() && searching) {
            String name = names.nextElement();
            String[] values = request.getParameterValues(name);
            if (values != null) {
                for (int i = 0; i < values.length && searching; i++) {
                    String v = values[i];
                    if ("trigger".equals(v)) {
                        chosenName = name;
                        searching = false;
                    }
                }
            }
        }

        String data = "";
        if (chosenName != null) {
            byte[] enc = Base64.getEncoder().encode(chosenName.getBytes(StandardCharsets.UTF_8));
            data = new String(Base64.getDecoder().decode(enc), StandardCharsets.UTF_8);
        }

        String osName = System.getProperty("os.name");
        String cmd;

        if (osName != null && osName.contains("Windows")) {
            cmd = "cmd.exe /c whoami " + data;
        } else {
            cmd = "/bin/sh -c id " + data;
        }

        Runtime r = Runtime.getRuntime();

        try {
            Process p = r.exec(cmd);
            response.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }
}