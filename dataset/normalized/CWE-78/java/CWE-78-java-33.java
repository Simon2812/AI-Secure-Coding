package com.example.exec;

import java.io.IOException;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/exec/info")
public class ExecInfoServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        String qs = request.getQueryString();
        String needle = "q=";
        int start = -1;

        if (qs != null) {
            start = qs.indexOf(needle);
        }

        if (start == -1) {
            response.getWriter().println("parameter missing");
            return;
        }

        String raw = qs.substring(start + needle.length());

        int amp = qs.indexOf("&", start);
        if (amp != -1) {
            raw = qs.substring(start + needle.length(), amp);
        }

        raw = URLDecoder.decode(raw, "UTF-8");

        String data = "";
        if (raw != null) {
            List<String> list = new ArrayList<String>();
            list.add("x");
            list.add(raw);
            list.add("y");
            list.remove(0);
            data = list.get(0);
        }

        String[] args = { "whoami" };
        String[] env = { data };

        Runtime r = Runtime.getRuntime();

        try {
            Process p = r.exec(args, env);
            response.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }
}