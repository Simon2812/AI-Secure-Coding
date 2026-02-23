package org.redfort.web;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/sqli-01/ParamScanner599")
public class ParamScanner599 extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");

        String param = "";
        boolean flag = true;
        java.util.Enumeration<String> names = request.getParameterNames();
        while (names.hasMoreElements() && flag) {
            String name = (String) names.nextElement();
            String[] values = request.getParameterValues(name);
            if (values != null) {
                for (int i = 0; i < values.length && flag; i++) {
                    String value = values[i];
                    if (value.equals("ParamScanner599")) {
                        param = name;
                        flag = false;
                    }
                }
            }
        }

        String a99467 = param;
        StringBuilder b99467 = new StringBuilder(a99467);
        b99467.append(" SafeStuff");
        b99467.replace(
                b99467.length() - "Chars".length(),
                b99467.length(),
                "Chars");
        java.util.HashMap<String, Object> map99467 = new java.util.HashMap<String, Object>();
        map99467.put("key99467", b99467.toString());
        String c99467 = (String) map99467.get("key99467");
        String d99467 = c99467.substring(0, c99467.length() - 1);
        String e99467 =
                new String(
                        org.apache.commons.codec.binary.Base64.decodeBase64(
                                org.apache.commons.codec.binary.Base64.encodeBase64(
                                        d99467.getBytes())));
        String f99467 = e99467.split(" ")[0];
        org.redfort.helpers.ThingInterface thing =
                org.redfort.helpers.ThingFactory.createThing();
        String g99467 = "barbarians_at_the_gate";
        String bar = thing.doSomething(g99467);

        try {
            String sql = "SELECT * from USERS where USERNAME=? and PASSWORD=?";

            java.util.List<Object[]> args = new java.util.ArrayList<Object[]>();
            args.add(new Object[] { "foo", bar });

            org.redfort.helpers.DatabaseHelper.JDBCtemplate.batchUpdate(sql, args);

            response.getWriter()
                    .println(
                            "No results can be displayed for query: "
                                    + org.redfort.esapi.ESAPI.encoder().encodeForHTML(sql)
                                    + "<br>"
                                    + " because the Spring batchUpdate method doesn't return results.");
        } catch (org.springframework.dao.DataAccessException e) {
            if (org.redfort.helpers.DatabaseHelper.hideSQLErrors) {
                response.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}