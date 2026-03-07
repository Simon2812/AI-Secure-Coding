package com.cyber.ops;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/ops/list")
public class ListServlet extends HttpServlet {

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
        String h = request.getHeader("X-Target");
        if (h != null) {
            headerValue = h;
        }

        headerValue = URLDecoder.decode(headerValue, StandardCharsets.UTF_8.name());

        String selected = "default";
        HashMap<String, Object> store = new HashMap<>();
        store.put("a", "x");
        store.put("b", headerValue);
        store.put("c", "y");
        selected = (String) store.get("b");

        String os = System.getProperty("os.name");
        String shell;
        String flag;
        if (os != null && os.contains("Windows")) {
            shell = "cmd.exe";
            flag = "/c";
        } else {
            shell = "sh";
            flag = "-c";
        }

        String[] cmd;
        if (os != null && os.contains("Windows")) {
            cmd = new String[] { shell, flag, "dir %DATA%" };
        } else {
            cmd = new String[] { shell, flag, "ls $DATA" };
        }

        String[] env = new String[] { "DATA=" + selected };

        Runtime rt = Runtime.getRuntime();

        try {
            Process p = rt.exec(cmd, env, new java.io.File(System.getProperty("user.dir")));
            response.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }
}