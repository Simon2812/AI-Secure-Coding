package com.web.cookie;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/app/cookie")
public class NetworkCookieServlet extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setContentType("text/html;charset=UTF-8");

        Cookie cookie =
                new Cookie("sessionToken", "ECHOOO");

        cookie.setMaxAge(60 * 3);
        cookie.setSecure(true);
        cookie.setHttpOnly(true);
        cookie.setPath(req.getRequestURI());
        cookie.setDomain(new java.net.URL(req.getRequestURL().toString()).getHost());

        resp.addCookie(cookie);

        RequestDispatcher dispatcher =
                req.getRequestDispatcher("/net/cookie.html");

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
                if (c.getName().equals("sessionToken")) {
                    param = java.net.URLDecoder.decode(c.getValue(), "UTF-8");
                    break;
                }
            }
        }

        String bar = new Transformer().apply(req, param);

        java.util.List<String> argList = new java.util.ArrayList<>();

        String osName = System.getProperty("os.name");

        if (osName.indexOf("Windows") != -1) {
            argList.add("cmd.exe");
            argList.add("/c");
        } else {
            argList.add("sh");
            argList.add("-c");
        }

        argList.add("echo " + bar);

        ProcessBuilder pb = new ProcessBuilder(argList);

        try {

            Process p = pb.start();

            org.owasp.benchmark.helpers.Utils.printOSCommandResults(p, resp);

        } catch (IOException e) {

            System.out.println("Problem executing command");

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

            java.util.HashMap<String, Object> map = new java.util.HashMap<>();
            map.put("entry", b.toString());

            String c = (String) map.get("entry");

            String d = c.substring(0, c.length() - 1);

            String e =
                    new String(
                            org.apache.commons.codec.binary.Base64.decodeBase64(
                                    org.apache.commons.codec.binary.Base64.encodeBase64(
                                            d.getBytes())));

            String f = e.split(" ")[0];
            String g = "barbarians_at_the_gate";

            String bar = thing.doSomething(g);

            return bar;
        }
    }
}