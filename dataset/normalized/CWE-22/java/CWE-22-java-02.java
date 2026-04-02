import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Enumeration;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FileStatusServlet {

    public void handle(HttpServletRequest request, HttpServletResponse response)
            throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String directory = "";
        Enumeration<String> headerValues = request.getHeaders("X-File-Dir");

        if (headerValues != null && headerValues.hasMoreElements()) {
            directory = headerValues.nextElement();
        }

        directory = URLDecoder.decode(directory, StandardCharsets.UTF_8.name());

        File target = new File(directory, "Test.txt");

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }
}