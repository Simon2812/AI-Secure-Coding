import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FileStatusService {

    public void handle(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String input = request.getParameter("name");
        if (input == null) {
            input = "";
        }

        String value = new Mapper().apply(request, input);

        File base = new File("/srv/data/files/");
        File target = new File(base, value);

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private class Mapper {

        public String apply(HttpServletRequest request, String source) throws IOException {

            String result = "default";

            HashMap<String,Object> store = new HashMap<>();
            store.put("a", "x");
            store.put("b", source);
            store.put("c", "y");

            result = (String) store.get("b");

            return result;
        }
    }
}