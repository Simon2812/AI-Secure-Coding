package web.session;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class CookieInspector {

    public void execute(HttpServletRequest request, HttpServletResponse response) throws Exception {

        String token = "";

        Cookie[] list = request.getCookies();
        if (list != null && list.length > 0) {
            token = list[0].getValue();
        }

        String command;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            command = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            command = "/bin/ls ";
        }

        Process p = Runtime.getRuntime().exec(command + token);
        p.waitFor();
    }
}