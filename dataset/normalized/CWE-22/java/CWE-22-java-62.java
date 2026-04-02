import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FileStatusController {

    public void handle(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String headerValue = "";
        String rawHeader = request.getHeader("X-Resource");

        if (rawHeader != null) {
            headerValue = rawHeader;
        }

        headerValue = URLDecoder.decode(headerValue, StandardCharsets.UTF_8.name());

        String selected;

        String seed = "ABC";
        char selector = seed.charAt(1);   // always 'B'

        switch (selector) {

            case 'A':
                selected = headerValue;
                break;

            case 'B':
                selected = "report.txt";
                break;

            case 'C':
            case 'D':
                selected = headerValue;
                break;

            default:
                selected = "default.txt";
                break;
        }

        File resolvedFile = new File(selected);

        response.getWriter().println("Access to file: '" + resolvedFile.toString() + "' created.");

        if (resolvedFile.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }
}