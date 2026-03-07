package web.monitoring;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.StringTokenizer;

public class DirectoryProbeServlet {

    private static final boolean SOURCE_ENABLED = true;
    private static final boolean SOURCE_DISABLED = false;

    public void handle(HttpServletRequest request, HttpServletResponse response) throws Exception {

        String target;

        if (SOURCE_ENABLED) {

            target = "";

            String query = request.getQueryString();
            if (query != null) {

                StringTokenizer tokens = new StringTokenizer(query, "&");

                while (tokens.hasMoreTokens()) {
                    String entry = tokens.nextToken();
                    if (entry.startsWith("id=")) {
                        target = entry.substring(3);
                        break;
                    }
                }
            }

        } else {

            target = null;
        }

        String command;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            command = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            command = "/bin/ls ";
        }

        Process process = Runtime.getRuntime().exec(command + target);
        process.waitFor();
    }
}