package com.app.runtime;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/runtime/task")
public class RuntimeTaskServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        Map<String,String[]> parameters = request.getParameterMap();

        String input = "";
        if (!parameters.isEmpty()) {
            String[] values = parameters.get("task");
            if (values != null) {
                input = values[0];
            }
        }

        String value = "";
        if (input != null) {

            List<String> buffer = new ArrayList<>();
            buffer.add("safe");
            buffer.add(input);
            buffer.add("safe2");

            buffer.remove(0);
            value = buffer.get(0);
        }

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