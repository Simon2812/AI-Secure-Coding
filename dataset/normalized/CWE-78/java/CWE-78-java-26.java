package com.example.tools;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/tools/info")
public class InfoServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        String headerValue = "";
        if (request.getHeader("X-Task") != null) {
            headerValue = request.getHeader("X-Task");
        }

        headerValue = URLDecoder.decode(headerValue, StandardCharsets.UTF_8.name());

        Processor proc = ProcessorFactory.create();
        String task = proc.process(headerValue);

        String shell = "";
        String flag = "";
        String os = System.getProperty("os.name");

        if (os != null && os.contains("Windows")) {
            shell = "cmd.exe";
            flag = "/c";
        } else {
            shell = "sh";
            flag = "-c";
        }

        String[] cmd = {shell, flag, "date " + task};

        ProcessBuilder builder = new ProcessBuilder(cmd);

        try {
            Process p = builder.start();
            response.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }
}