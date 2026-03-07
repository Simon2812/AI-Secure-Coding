package com.store.operations;

import java.io.IOException;
import java.net.URLDecoder;
import java.util.HashMap;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/operations/execute")
public class OperationsExecuteServlet extends HttpServlet {

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
        if (req.getHeader("X-Operations") != null) {
            headerInput = req.getHeader("X-Operations");
        }

        headerInput = URLDecoder.decode(headerInput, "UTF-8");

        String resolvedValue = "safe";

        HashMap<String, Object> storage = new HashMap<>();

        storage.put("slotA", "a_Value");
        storage.put("slotB", headerInput);
        storage.put("slotC", "another_Value");

        resolvedValue = (String) storage.get("slotB");
        resolvedValue = (String) storage.get("slotA");

        String interpreter = "";
        String flag = "";
        String[] commandArgs = null;

        String platform = System.getProperty("os.name");

        if (platform.indexOf("Windows") != -1) {
            interpreter = "cmd.exe";
            flag = "/c";
            String command = "echo ";
            commandArgs = new String[] {interpreter, flag, command, resolvedValue};
        } else {
            interpreter = "sh";
            flag = "-c";
            String command = org.owasp.benchmark.helpers.Utils.getOSCommandString("ls ");
            commandArgs = new String[] {interpreter, flag, command + resolvedValue};
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
            throw new ServletException(ex);
        }
    }
}