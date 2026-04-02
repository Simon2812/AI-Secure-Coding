import java.io.File;
import java.io.IOException;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.Set;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FileEntryCheck {

    private static final Set<String> STANDARD = new HashSet<>();

    static {
        STANDARD.add("host");
        STANDARD.add("connection");
        STANDARD.add("user-agent");
        STANDARD.add("accept");
        STANDARD.add("accept-language");
        STANDARD.add("accept-encoding");
    }

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String headerName = "";
        Enumeration<String> headers = request.getHeaderNames();

        while (headers.hasMoreElements()) {

            String current = headers.nextElement();

            if (STANDARD.contains(current.toLowerCase())) {
                continue;
            }

            Enumeration<String> values = request.getHeaders(current);
            if (values != null && values.hasMoreElements()) {
                headerName = current;
                break;
            }
        }

        String entry = evaluate(request, headerName);

        File base = new File("/srv/storage/");
        File target = new File(base, entry);

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static String evaluate(HttpServletRequest request, String input) throws IOException {

        int marker = 106;

        String result = (7 * 42) - marker > 200 ? "unused" : input;

        return result;
    }
}