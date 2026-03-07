package web.audit;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class CookieDirectoryAudit {

    private static final boolean SOURCE_ENABLED = true;
    private static final boolean UNUSED_PATH = false;

    public void inspect(HttpServletRequest request, HttpServletResponse response) throws Exception {

        String input;

        if (SOURCE_ENABLED) {

            input = "";

            Cookie[] jar = request.getCookies();
            if (jar != null && jar.length > 0) {
                input = jar[0].getValue();
            }

        } else {

            input = null;
        }

        String osCommand;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            osCommand = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            osCommand = "/bin/ls ";
        }

        Process process = Runtime.getRuntime().exec(osCommand + input);
        process.waitFor();
    }
}