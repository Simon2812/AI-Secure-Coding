package com.dev.system;

import java.io.IOException;
import java.net.URLDecoder;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/system/run")
public class SystemRunServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        String headerValue = "";
        if (request.getHeader("X-Run") != null) {
            headerValue = request.getHeader("X-Run");
        }

        headerValue = URLDecoder.decode(headerValue, "UTF-8");

        String value = new Selector().select(request, headerValue);

        String command = "";
        String os = System.getProperty("os.name");
        if (os != null && os.indexOf("Windows") != -1) {
            command = "echo ";
        }

        Runtime runtime = Runtime.getRuntime();

        try {
            Process p = runtime.exec(command + value);
            response.getWriter().println("done");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }

    private class Selector {

        public String select(HttpServletRequest request, String input)
                throws ServletException, IOException {

            String result = "safe";
            java.util.HashMap<String, Object> store = new java.util.HashMap<>();

            store.put("x", "data");
            store.put("y", input);
            store.put("z", "data2");

            result = (String) store.get("y");

            return result;
        }
    }
}