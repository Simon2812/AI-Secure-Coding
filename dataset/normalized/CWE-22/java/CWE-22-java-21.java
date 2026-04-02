import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FileProbe {

    public void handle(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String header = "";
        if (request.getHeader("X-Path") != null) {
            header = request.getHeader("X-Path");
        }

        header = URLDecoder.decode(header, StandardCharsets.UTF_8.name());

        String path = transform(request, header);

        File target = new File(path);

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static String transform(HttpServletRequest request, String value) throws IOException {

        String result = "default";

        HashMap<String,Object> map = new HashMap<>();
        map.put("a", "one");
        map.put("b", value);
        map.put("c", "two");

        result = (String) map.get("b");

        return result;
    }
}