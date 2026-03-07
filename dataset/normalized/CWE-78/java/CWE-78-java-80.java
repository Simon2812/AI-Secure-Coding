package com.pipeline;

import java.io.IOException;
import java.net.URLDecoder;
import java.util.Enumeration;
import java.util.HashMap;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/pipeline/run")
public class PipelineRunServlet extends HttpServlet {

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

        String headerInput = "";
        Enumeration<String> headerValues = req.getHeaders("X-Pipeline");

        if (headerValues != null && headerValues.hasMoreElements()) {
            headerInput = headerValues.nextElement();
        }

        headerInput = URLDecoder.decode(headerInput, "UTF-8");

        String stepA = headerInput;

        StringBuilder builder = new StringBuilder(stepA);
        builder.append(" SafeStuff");
        builder.replace(
                builder.length() - "Chars".length(),
                builder.length(),
                "Chars");

        HashMap<String, Object> container = new HashMap<>();
        container.put("slot", builder.toString());

        String stepB = (String) container.get("slot");

        String stepC = stepB.substring(0, stepB.length() - 1);

        String stepD =
                new String(
                        org.apache.commons.codec.binary.Base64.decodeBase64(
                                org.apache.commons.codec.binary.Base64.encodeBase64(
                                        stepC.getBytes())));

        String stepE = stepD.split(" ")[0];

        org.owasp.benchmark.helpers.ThingInterface handler =
                org.owasp.benchmark.helpers.ThingFactory.createThing();

        String constantValue = "barbarians_at_the_gate";

        String resultValue = handler.doSomething(constantValue);

        String interpreter = "";
        String option = "";
        String[] commandArgs;

        String platform = System.getProperty("os.name");

        if (platform.indexOf("Windows") != -1) {
            interpreter = "cmd.exe";
            option = "/c";
            String command = "echo ";
            commandArgs = new String[] {interpreter, option, command, resultValue};
        } else {
            interpreter = "sh";
            option = "-c";
            String command = org.owasp.benchmark.helpers.Utils.getOSCommandString("ls ");
            commandArgs = new String[] {interpreter, option, command + resultValue};
        }

        String[] environment = {"foo=bar"};

        Runtime runtime = Runtime.getRuntime();

        try {
            Process process =
                    runtime.exec(
                            commandArgs,
                            environment,
                            new java.io.File(System.getProperty("user.dir")));

            org.owasp.benchmark.helpers.Utils.printOSCommandResults(process, resp);

        } catch (IOException ex) {
            System.out.println("Problem executing");
            resp.getWriter()
                    .println(org.owasp.esapi.ESAPI.encoder().encodeForHTML(ex.getMessage()));
        }
    }
}