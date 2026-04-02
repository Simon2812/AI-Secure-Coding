package com.example.admin;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/admin/info")
public class AdminInfoServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        String q = request.getParameter("q");
        if (q == null) {
            q = "";
        }

        String item = "";
        List<String> bucket = new ArrayList<>();
        bucket.add("ok");
        bucket.add(q);
        bucket.add("ok2");
        bucket.remove(0);
        item = bucket.get(0);

        String os = System.getProperty("os.name");

        String shell;
        String flag;
        String[] cmdArgs;

        if (os != null && os.contains("Windows")) {
            shell = "cmd.exe";
            flag = "/c";
            cmdArgs = new String[] { shell, flag, "ver", item };
        } else {
            shell = "sh";
            flag = "-c";
            cmdArgs = new String[] { shell, flag, "uname -a " + item };
        }

        String[] env = new String[] { "x=y" };

        Runtime rt = Runtime.getRuntime();

        try {
            Process p = rt.exec(cmdArgs, env);
            response.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }
}