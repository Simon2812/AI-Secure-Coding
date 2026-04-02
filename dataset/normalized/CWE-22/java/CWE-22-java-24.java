import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FileAccessService {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String input = request.getParameter("path");
        if (input == null) {
            input = "";
        }

        String name = transform(input);

        File base = new File("/srv/storage/");
        File target = new File(base, name);

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static String transform(String value) {

        String result = "";

        if (value != null) {
            List<String> list = new ArrayList<>();
            list.add("safe");
            list.add(value);
            list.add("other");

            list.remove(0);

            result = list.get(0);
        }

        return result;
    }
}