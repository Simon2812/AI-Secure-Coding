import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.codec.binary.Base64;

public class FileQueryInspector {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String query = request.getQueryString();
        String marker = "path=";
        int position = -1;

        if (query != null) {
            position = query.indexOf(marker);
        }

        if (position == -1) {
            response.getWriter().println("Parameter not found.");
            return;
        }

        String raw = query.substring(position + marker.length());

        int next = query.indexOf("&", position);
        if (next != -1) {
            raw = query.substring(position + marker.length(), next);
        }

        raw = URLDecoder.decode(raw, StandardCharsets.UTF_8.name());

        String candidate = transform(raw);

        File fileRef = new File(candidate);

        response.getWriter().println("Access to file: '" + fileRef.toString() + "' created.");

        if (fileRef.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static String transform(String input) {

        String result = "";

        if (input != null) {
            result = new String(Base64.decodeBase64(Base64.encodeBase64(input.getBytes())));
        }

        return result;
    }
}