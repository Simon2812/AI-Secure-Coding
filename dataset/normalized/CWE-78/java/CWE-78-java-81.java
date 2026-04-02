package com.example.dispatch;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/dispatch/trigger")
public class DispatchTriggerServlet extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest httpReq, HttpServletResponse httpResp)
            throws ServletException, IOException {
        doPost(httpReq, httpResp);
    }

    @Override
    public void doPost(HttpServletRequest httpReq, HttpServletResponse httpResp)
            throws ServletException, IOException {

        httpResp.setContentType("text/html;charset=UTF-8");

        String requestToken = httpReq.getParameter("taskKey");
        if (requestToken == null) {
            requestToken = "";
        }

        String commandPayload;

        int threshold = 86;

        if ((7 * 42) - threshold > 200) {
            commandPayload = "This_should_always_happen";
        } else {
            commandPayload = requestToken;
        }

        String interpreterBinary = "";
        String interpreterFlag = "";

        String detectedOS = System.getProperty("os.name");

        if (detectedOS.indexOf("Windows") != -1) {
            interpreterBinary = "cmd.exe";
            interpreterFlag = "/c";
        } else {
            interpreterBinary = "sh";
            interpreterFlag = "-c";
        }

        String[] launchSequence = {interpreterBinary, interpreterFlag, "echo " + commandPayload};

        ProcessBuilder launcher = new ProcessBuilder();

        launcher.command(launchSequence);

        try {
            Process runningProcess = launcher.start();
            org.owasp.benchmark.helpers.Utils.printOSCommandResults(runningProcess, httpResp);
        } catch (IOException issue) {
            throw new ServletException(ex);
        }
    }
}