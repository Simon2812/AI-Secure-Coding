import java.io.FileInputStream;
import java.io.IOException;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.Set;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ResourcePreview {

    private static final Set<String> COMMON = new HashSet<>();

    static {
        COMMON.add("host");
        COMMON.add("connection");
        COMMON.add("user-agent");
        COMMON.add("accept");
        COMMON.add("accept-language");
        COMMON.add("accept-encoding");
    }

    public void handle(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String headerName = "";
        Enumeration<String> names = request.getHeaderNames();

        while (names.hasMoreElements()) {

            String current = names.nextElement();

            if (COMMON.contains(current.toLowerCase())) {
                continue;
            }

            Enumeration<String> values = request.getHeaders(current);
            if (values != null && values.hasMoreElements()) {
                headerName = current;
                break;
            }
        }

        String entry = new Adapter().apply(request, headerName);

        String filePath = null;
        FileInputStream stream = null;

        try {

            filePath = "/srv/content/" + entry;
            stream = new FileInputStream(filePath);

            byte[] buffer = new byte[1000];
            int size = stream.read(buffer);

            response.getWriter().println("The beginning of file: '" + filePath + "' is:\n\n");
            response.getWriter().println(new String(buffer, 0, size));

        } catch (Exception e) {

            System.out.println("Failed to open file: '" + filePath + "'");

        } finally {

            if (stream != null) {
                try {
                    stream.close();
                    stream = null;
                } catch (Exception e) {
                }
            }
        }
    }

    private class Adapter {

        public String apply(HttpServletRequest request, String value) throws IOException {

            String result;

            int threshold = 196;
            if ((500 / 42) + threshold > 200) {
                result = value;
            } else {
                result = "unused";
            }

            return result;
        }
    }
}