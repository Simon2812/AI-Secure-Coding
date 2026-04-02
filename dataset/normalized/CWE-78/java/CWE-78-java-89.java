package com.app.gateway;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/gateway/header")
public class HeaderGatewayServlet extends HttpServlet {

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

        String param = "";

        if (req.getHeader("node") != null) {
            param = req.getHeader("node");
        }

        param = java.net.URLDecoder.decode(param, "UTF-8");

        String bar = new Transformer().apply(req, param);

        String cmd = "";
        String a1 = "";
        String a2 = "";
        String[] args = null;

        String osName = System.getProperty("os.name");

        if (osName.indexOf("Windows") != -1) {

            a1 = "cmd.exe";
            a2 = "/c";
            cmd = "echo";

            args = new String[]{a1, a2, cmd, bar};

        } else {

            a1 = "sh";
            a2 = "-c";
            cmd = "ping -c1 ";

            args = new String[]{a1, a2, cmd + bar};
        }

        Runtime runtime = Runtime.getRuntime();

        try {

            Process p = runtime.exec(args);

            resp.getWriter().println("ok");

        } catch (IOException e) {

            throw new ServletException(e);
        }
    }

    private class Transformer {

        public String apply(HttpServletRequest req, String param)
                throws ServletException, IOException {

            String bar;

            int num = 86;

            if ((7 * 42) - num > 200)
                bar = "This_should_always_happen";
            else
                bar = param;

            return bar;
        }
    }
}