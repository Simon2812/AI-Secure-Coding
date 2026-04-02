import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ArchiveInspector {

    public void run(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        ParameterReader reader = new ParameterReader(request);
        String value = reader.get("entry");
        if (value == null) {
            value = "";
        }

        String name = "";
        if (value != null) {

            List<String> items = new ArrayList<>();
            items.add("fixed");
            items.add(value);
            items.add("backup");

            items.remove(0);

            name = items.get(0);
        }

        File root = new File("/var/service/archive/");
        File resource = new File(root, name);

        response.getWriter().println("Access to file: '" + resource.toString() + "' created.");

        if (resource.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }
}