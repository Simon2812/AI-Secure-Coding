package com.app.module;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/module/task")
public class TaskHandlerServlet extends HttpServlet {

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

        org.owasp.benchmark.helpers.SeparateClassRequest extractor =
                new org.owasp.benchmark.helpers.SeparateClassRequest(req);

        String inputValue = extractor.getTheValue("BenchmarkTest00051");

        String interpreter = "";
        String option = "";

        String platform = System.getProperty("os.name");

        if (platform.indexOf("Windows") != -1) {
            interpreter = "cmd.exe";
            option = "/c";
        } else {
            interpreter = "sh";
            option = "-c";
        }

        String[] commandArgs = {interpreter, option, "echo " + inputValue};

        ProcessBuilder builder = new ProcessBuilder(commandArgs);

        try {
            Process proc = builder.start();
            org.owasp.benchmark.helpers.Utils.printOSCommandResults(proc, resp);
        } catch (IOException ex) {
            throw new ServletException(ex)
        }
    }
}