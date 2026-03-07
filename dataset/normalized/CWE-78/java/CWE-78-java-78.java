package com.task.executor;

import java.io.IOException;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/executor/run")
public class ExecutorRunServlet extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    public void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setContentType("text/html;charset=UTF-8");

        String headerValue = "";

        if (req.getHeader("X-Executor") != null) {
            headerValue = req.getHeader("X-Executor");
        }

        headerValue = URLDecoder.decode(headerValue, "UTF-8");

        String resolvedValue;

        int marker = 86;

        if ((7 * 42) - marker > 200) {
            resolvedValue = "This_should_always_happen";
        } else {
            resolvedValue = headerValue;
        }

        List<String> commandParts = new ArrayList<>();

        String systemName = System.getProperty("os.name");

        if (systemName.indexOf("Windows") != -1) {
            commandParts.add("cmd.exe");
            commandParts.add("/c");
        } else {
            commandParts.add("sh");
            commandParts.add("-c");
        }

        commandParts.add("echo " + resolvedValue);

        ProcessBuilder builder = new ProcessBuilder(commandParts);

        try {
            Process process = builder.start();
            org.owasp.benchmark.helpers.Utils.printOSCommandResults(process, resp);
        } catch (IOException ex) {
            throw new ServletException(ex);
        }
    }
}