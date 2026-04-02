package com.web.identity;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Enumeration;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/identity/check")
public class IdentityServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/plain;charset=UTF-8");

        String headerData = "";
        Enumeration<String> values = request.getHeaders("X-Trace");

        if (values != null && values.hasMoreElements()) {
            headerData = values.nextElement();
        }

        headerData = URLDecoder.decode(headerData, StandardCharsets.UTF_8.name());

        String payload;

        int seed = 106;
        payload = (7 * 42) - seed > 200 ? "unused" : headerData;

        String os = System.getProperty("os.name");
        String baseCmd;

        if (os != null && os.contains("Windows")) {
            baseCmd = "whoami";
        } else {
            baseCmd = "id";
        }

        ProcessBuilder builder = new ProcessBuilder(baseCmd, payload);

        try {
            Process p = builder.start();
            response.getWriter().println("ok");
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }
}