package com.gateway.edge;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/edge/gateway")
public class GatewayServlet extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setContentType("text/html;charset=UTF-8");

        Cookie cookie = new Cookie("node", "localhost");

        cookie.setMaxAge(60 * 3);
        cookie.setSecure(true);
        cookie.setHttpOnly(true);
        cookie.setPath(req.getRequestURI());
        cookie.setDomain(new java.net.URL(req.getRequestURL().toString()).getHost());

        resp.addCookie(cookie);

        RequestDispatcher dispatcher =
                req.getRequestDispatcher("/edge/gateway.html");

        dispatcher.include(req, resp);
    }

    @Override
    public void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setContentType("text/html;charset=UTF-8");

        Cookie[] cookies = req.getCookies();

        String param = "noCookieValueSupplied";

        if (cookies != null) {
            for (Cookie c : cookies) {
                if (c.getName().equals("node")) {
                    param = java.net.URLDecoder.decode(c.getValue(), "UTF-8");
                    break;
                }
            }
        }

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
            args = new String[] {a1, a2, cmd, bar};
        } else {
            a1 = "sh";
            a2 = "-c";
            cmd = "ping -c1 ";
            args = new String[] {a1, a2, cmd + bar};
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

            String a = param;

            StringBuilder b = new StringBuilder(a);
            b.append(" SafeStuff");

            b.replace(
                    b.length() - "Chars".length(),
                    b.length(),
                    "Chars");

            java.util.HashMap<String, Object> store = new java.util.HashMap<>();
            store.put("slot", b.toString());

            String c = (String) store.get("slot");

            String d = c.substring(0, c.length() - 1);

            String e =
                    new String(
                            org.apache.commons.codec.binary.Base64.decodeBase64(
                                    org.apache.commons.codec.binary.Base64.encodeBase64(
                                            d.getBytes())));

            String f = e.split(" ")[0];

            Handler handler = new Handler();

            String g = "barbarians_at_the_gate";

            String bar = handler.process(g);

            return bar;
        }
    }

    private class Handler {

        public String process(String input) {
            return input;
        }
    }
}