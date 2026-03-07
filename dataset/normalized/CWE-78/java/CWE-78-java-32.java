package com.example.task;

import java.io.IOException;
import java.util.HashMap;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/task/run")
public class TaskRunnerServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        String[] inputs = request.getParameterValues("task");
        String input;

        if (inputs != null && inputs.length > 0) {
            input = inputs[0];
        } else {
            input = "";
        }

        String value = "safe";

        HashMap<String,Object> store = new HashMap<>();
        store.put("k1", "v1");
        store.put("k2", input);
        store.put("k3", "v2");

        value = (String) store.get("k2");

        String command = "whoami";

        String[] args = { command };
        String[] env = { value };

        Runtime runtime = Runtime.getRuntime();

        try {
            Process p = runtime.exec(args, env);
            response.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }
}