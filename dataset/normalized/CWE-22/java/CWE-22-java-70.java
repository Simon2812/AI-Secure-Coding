import java.io.FileInputStream;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FilePreviewService {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String headerValue = "";
        Enumeration<String> headerStream = request.getHeaders("X-Resource");

        if (headerStream != null && headerStream.hasMoreElements()) {
            headerValue = headerStream.nextElement();
        }

        headerValue = URLDecoder.decode(headerValue, StandardCharsets.UTF_8.name());

        String selected = new Resolver().resolve(headerValue);

        String path = null;
        FileInputStream stream = null;

        try {

            path = "/srv/storage/" + selected;

            stream = new FileInputStream(path);

            byte[] buffer = new byte[1000];
            int size = stream.read(buffer);

            response.getWriter().println(
                    "The beginning of file: '" + path + "' is:\n\n"
            );

            response.getWriter().println(
                    new String(buffer, 0, size)
            );

        } catch (Exception e) {

            System.out.println("Couldn't open FileInputStream on file: '" + path + "'");

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

    private static class Resolver {

        public String resolve(String value) {

            String result = "static.txt";

            if (value != null) {

                List<String> container = new ArrayList<>();

                container.add("safe");
                container.add(value);
                container.add("static.txt");

                container.remove(0);

                result = container.get(1);
            }

            return result;
        }
    }
}