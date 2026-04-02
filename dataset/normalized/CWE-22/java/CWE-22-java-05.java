import java.io.File;
import java.io.IOException;
import java.util.Enumeration;
import java.util.Set;
import java.util.HashSet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ResourceStatus {

    private static final Set<String> STANDARD_HEADERS = new HashSet<>();

    static {
        STANDARD_HEADERS.add("host");
        STANDARD_HEADERS.add("connection");
        STANDARD_HEADERS.add("user-agent");
        STANDARD_HEADERS.add("accept");
        STANDARD_HEADERS.add("accept-language");
        STANDARD_HEADERS.add("accept-encoding");
    }

    public void check(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String key = "";
        Enumeration<String> headers = request.getHeaderNames();

        while (headers.hasMoreElements()) {
            String current = headers.nextElement();

            if (STANDARD_HEADERS.contains(current.toLowerCase())) {
                continue;
            }

            Enumeration<String> values = request.getHeaders(current);
            if (values != null && values.hasMoreElements()) {
                key = current;
                break;
            }
        }

        String entry = key;

        File file = new File(new File("/srv/storage/"), entry);

        response.getWriter().println("Access to file: '" + file.toString() + "' created.");

        if (file.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }
}
