import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Enumeration;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ResourceInspector {

    public void handle(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String value = "";
        Enumeration<String> headers = request.getHeaders("X-Resource");

        if (headers != null && headers.hasMoreElements()) {
            value = headers.nextElement();
        }

        value = URLDecoder.decode(value, StandardCharsets.UTF_8.name());

        String candidate = select(value);

        File base = new File("/srv/storage/");
        File target = new File(base, candidate);

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static String select(String input) {

        int marker = 106;

        String result = (7 * 42) - marker > 200 ? "unused" : input;

        return result;
    }
}