import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FileLocator {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        Cookie[] cookies = request.getCookies();

        String token = "default";
        if (cookies != null) {
            for (Cookie c : cookies) {
                if ("recent".equals(c.getName())) {
                    token = URLDecoder.decode(c.getValue(), StandardCharsets.UTF_8.name());
                    break;
                }
            }
        }

        String name = new Resolver().resolve(request, token);

        File root = new File("/var/data/files/");
        File item = new File(root, name);

        response.getWriter().println("Access to file: '" + item.toString() + "' created.");

        if (item.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private class Resolver {

        public String resolve(HttpServletRequest request, String value) throws IOException {
            String result = value;
            return result;
        }
    }
}