import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FileLookupService {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        Cookie[] cookies = request.getCookies();

        String value = "none";
        if (cookies != null) {
            for (Cookie c : cookies) {
                if ("resource".equals(c.getName())) {
                    value = URLDecoder.decode(c.getValue(), StandardCharsets.UTF_8.name());
                    break;
                }
            }
        }

        String entry = transform(value);

        File rootDir = new File("/srv/storage/");
        File target = new File(rootDir, entry);

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static String transform(String input) {

        String result = "safe";

        HashMap<String,Object> map = new HashMap<>();
        map.put("a", "one");
        map.put("b", input);
        map.put("c", "two");

        result = (String) map.get("b");

        return result;
    }
}