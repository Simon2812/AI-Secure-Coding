import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ResourceLocationService {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        RequestWrapper wrapper = new RequestWrapper(request);
        String input = wrapper.getValue("path");

        if (input == null) {
            input = "";
        }

        String chosen = "constant";

        if (input != null) {

            List<String> container = new ArrayList<>();
            container.add("first");
            container.add(input);
            container.add("fixed");

            container.remove(0);

            chosen = container.get(1);
        }

        File dataRoot = new File("/srv/storage/");
        File fileRef = new File(dataRoot, chosen);

        response.getWriter().println("Access to file: '" + fileRef.toString() + "' created.");

        if (fileRef.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static class RequestWrapper {

        private final HttpServletRequest request;

        RequestWrapper(HttpServletRequest request) {
            this.request = request;
        }

        public String getValue(String key) {
            return request.getParameter(key);
        }
    }
}