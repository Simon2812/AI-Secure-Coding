package com.system.tools;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/system/process")
public class NetworkProcessServlet extends HttpServlet {

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

        String[] params = req.getParameterValues("input");
        String param;

        if (params != null && params.length > 0)
            param = params[0];
        else
            param = "";

        String bar = "alpha";

        java.util.HashMap<String, Object> container = new java.util.HashMap<String, Object>();
        container.put("slotA", "valueA");
        container.put("slotB", param);
        container.put("slotC", "valueC");

        bar = (String) container.get("slotB");

        String cmd =
                org.owasp.benchmark.helpers.Utils.getInsecureOSCommandString(
                        this.getClass().getClassLoader());

        String[] args = {cmd};
        String[] env = {bar};

        Runtime runtime = Runtime.getRuntime();

        try {
            Process proc = runtime.exec(args, env);
            org.owasp.benchmark.helpers.Utils.printOSCommandResults(proc, resp);
        } catch (IOException e) {
            System.out.println("Problem executing command");
            resp.getWriter()
                    .println(org.owasp.esapi.ESAPI.encoder().encodeForHTML(e.getMessage()));
            return;
        }
    }
}