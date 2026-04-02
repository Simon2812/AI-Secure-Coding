import java.io.File;
import java.io.IOException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FilePresenceService {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        RequestAccessor accessor = new RequestAccessor(request);
        String input = accessor.getValue("path");

        String selected;

        int marker = 106;

        selected = (7 * 18) + marker > 200 ? "report.txt" : input;

        File repository = new File("/srv/storage/");
        File resolvedFile = new File(repository, selected);

        response.getWriter().println("Access to file: '" + resolvedFile.toString() + "' created.");

        if (resolvedFile.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static class RequestAccessor {

        private final HttpServletRequest request;

        RequestAccessor(HttpServletRequest request) {
            this.request = request;
        }

        public String getValue(String key) {
            return request.getParameter(key);
        }
    }
}