package web.tools;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class DirectoryEndpoint {

    public void handle(HttpServletRequest request, HttpServletResponse response) throws Exception {

        String value = request.getParameter("name");

        String cmd;
        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            cmd = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            cmd = "/bin/ls ";
        }

        Process process = Runtime.getRuntime().exec(cmd + value);
        process.waitFor();
    }
}