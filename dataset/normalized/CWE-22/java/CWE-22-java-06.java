import java.io.File;
import java.io.IOException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class StorageProbe {

    public void handle(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String value = request.getParameter("file");
        if (value == null) {
            value = "";
        }

        String candidate;

        int limit = 196;
        if ((500 / 42) + limit > 200) {
            candidate = value;
        } else {
            candidate = "unused";
        }

        File resource = new File(candidate);

        response.getWriter().println("Access to file: '" + resource.toString() + "' created.");

        if (resource.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }
}