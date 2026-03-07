package com.api.gateway;

import java.io.IOException;
import java.net.URLDecoder;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/gateway/action")
public class GatewayActionServlet extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setContentType("text/html;charset=UTF-8");

        Cookie cookie =
                new Cookie("GatewayActionCookie", "ls");

        cookie.setMaxAge(60 * 3);
        cookie.setSecure(true);
        cookie.setHttpOnly(true);
        cookie.setPath(req.getRequestURI());
        cookie.setDomain(new java.net.URL(req.getRequestURL().toString()).getHost());

        resp.addCookie(cookie);

        javax.servlet.RequestDispatcher dispatcher =
                req.getRequestDispatcher("/cmdi-00/BenchmarkTest00090.html");

        dispatcher.include(req, resp);
    }

    @Override
    public void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setContentType("text/html;charset=UTF-8");

        Cookie[] cookieList = req.getCookies();

        String inputValue = "noCookieValueSupplied";

        if (cookieList != null) {
            for (Cookie c : cookieList) {
                if (c.getName().equals("GatewayActionCookie")) {
                    inputValue = URLDecoder.decode(c.getValue(), "UTF-8");
                    break;
                }
            }
        }

        String resultValue;

        int marker = 86;

        if ((7 * 42) - marker > 200) {
            resultValue = "This_should_always_happen";
        } else {
            resultValue = inputValue;
        }

        String command = "";

        String systemName = System.getProperty("os.name");

        if (systemName.indexOf("Windows") != -1) {
            command = org.owasp.benchmark.helpers.Utils.getOSCommandString("echo");
        }

        Runtime runtime = Runtime.getRuntime();

        try {
            Process proc = runtime.exec(command + resultValue);
            org.owasp.benchmark.helpers.Utils.printOSCommandResults(proc, resp);
        } catch (IOException ex) {
            throw new ServletException(ex);
        }
    }
}