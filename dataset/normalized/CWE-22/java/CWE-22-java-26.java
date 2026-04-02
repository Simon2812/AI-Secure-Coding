import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FileQueryService {

    public void execute(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        Map<String,String[]> parameters = request.getParameterMap();

        String input = "";
        if (!parameters.isEmpty()) {
            String[] values = parameters.get("path");
            if (values != null) {
                input = values[0];
            }
        }

        String name = transform(input);

        File dataRoot = new File("/srv/storage/");
        File resolvedFile = new File(dataRoot, name);

        response.getWriter().println("Access to file: '" + resolvedFile.toString() + "' created.");

        if (resolvedFile.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static String transform(String value) {

        String result = "safe";

        HashMap<String,Object> container = new HashMap<>();
        container.put("x", "alpha");
        container.put("y", value);
        container.put("z", "beta");

        result = (String) container.get("y");

        return result;
    }
}