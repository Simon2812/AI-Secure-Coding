package com.example.web;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/tools/preview")
public class PreviewServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        String value = request.getHeader("X-Note");
        if (value == null) {
            value = "";
        }
        value = URLDecoder.decode(value, StandardCharsets.UTF_8.name());

        List<String> cmd = new ArrayList<>();
        String osName = System.getProperty("os.name");

        if (osName != null && osName.contains("Windows")) {
            cmd.add("cmd.exe");
            cmd.add("/c");
        } else {
            cmd.add("sh");
            cmd.add("-c");
        }

        cmd.add("echo " + value);

        ProcessBuilder pb = new ProcessBuilder();
        pb.command(cmd);

        try {
            Process p = pb.start();
            response.getWriter().println("OK");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }
}