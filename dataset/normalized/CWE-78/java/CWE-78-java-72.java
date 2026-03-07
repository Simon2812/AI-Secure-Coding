package aurora.http.directory;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class CookieDirectoryController
{

    public static void handle(HttpServletRequest req, HttpServletResponse res) throws Exception
    {
        String cookieValue = "";

        Cookie[] jar = req.getCookies();

        if (jar != null && jar.length > 0)
        {
            cookieValue = jar[0].getValue();
        }

        if (cookieValue == null)
        {
            cookieValue = "";
        }

        Process task;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            task = new ProcessBuilder("cmd.exe", "/c", "dir", cookieValue).start();
        }
        else
        {
            task = new ProcessBuilder("/bin/ls", cookieValue).start();
        }

        task.waitFor();
    }
}