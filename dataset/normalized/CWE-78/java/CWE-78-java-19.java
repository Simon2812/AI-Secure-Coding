package web.handlers;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.StringTokenizer;

public class QueryInspectorServlet {

    public void service(HttpServletRequest request, HttpServletResponse response) throws Exception {

        String idValue = "";

        String qs = request.getQueryString();
        if (qs != null) {
            StringTokenizer parts = new StringTokenizer(qs, "&");
            while (parts.hasMoreTokens()) {
                String pair = parts.nextToken();
                if (pair.startsWith("id=")) {
                    idValue = pair.substring(3);
                    break;
                }
            }
        }

        String osCommand;
        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            osCommand = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            osCommand = "/bin/ls ";
        }

        Process process = Runtime.getRuntime().exec(osCommand + idValue);
        process.waitFor();
    }
}