import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class DocumentCheck {

    public void handle(HttpServletRequest request, HttpServletResponse response)
            throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        Cookie[] cookies = request.getCookies();

        String value = "default.txt";
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("recentFile".equals(cookie.getName())) {
                    value = URLDecoder.decode(cookie.getValue(), StandardCharsets.UTF_8.name());
                    break;
                }
            }
        }

        String name = "";
        if (value != null) {
            name = new String(Base64.getDecoder().decode(Base64.getEncoder().encode(value.getBytes())));
        }

        File target = new File(new File("/var/app/data/"), name);

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }
}