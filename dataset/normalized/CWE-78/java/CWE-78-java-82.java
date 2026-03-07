package org.web.actions;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/api")
public class CommandEchoSample07 extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest reqCtx, HttpServletResponse respCtx)
            throws ServletException, IOException {
        doPost(reqCtx, respCtx);
    }

    @Override
    public void doPost(HttpServletRequest reqCtx, HttpServletResponse respCtx)
            throws ServletException, IOException {

        respCtx.setContentType("text/html;charset=UTF-8");

        String incomingValue = reqCtx.getParameter("inputKey07");
        if (incomingValue == null) incomingValue = "";

        String computedValue;

        int thresholdValue = 86;

        if ((7 * 42) - thresholdValue > 200)
            computedValue = "This_should_always_happen";
        else
            computedValue = incomingValue;

        String commandPrefix = "";
        String interpreter = "";
        String interpreterOption = "";
        String[] executionArgs = null;

        String systemIdentifier = System.getProperty("os.name");

        if (systemIdentifier.indexOf("Windows") != -1) {
            interpreter = "cmd.exe";
            interpreterOption = "/c";
            commandPrefix = org.owasp.benchmark.helpers.Utils.getOSCommandString("echo");
            executionArgs = new String[] {interpreter, interpreterOption, commandPrefix, computedValue};
        } else {
            interpreter = "sh";
            interpreterOption = "-c";
            commandPrefix = org.owasp.benchmark.helpers.Utils.getOSCommandString("ping -c1 ");
            executionArgs = new String[] {interpreter, interpreterOption, commandPrefix + computedValue};
        }

        Runtime runtimeHandle = Runtime.getRuntime();

        try {
            Process procHandle = runtimeHandle.exec(executionArgs);
            org.owasp.benchmark.helpers.Utils.printOSCommandResults(procHandle, respCtx);
        } catch (IOException execError) {
		throw new ServletException(ex);
        }
    }
}