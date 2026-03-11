import java.io.File;
import java.io.IOException;
import java.util.Enumeration;
import java.util.HashMap;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FileLookupService {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String headerKey = "";

        Enumeration<String> headerNames = request.getHeaderNames();

        while (headerNames.hasMoreElements()) {
            String name = headerNames.nextElement();

            if (name.equalsIgnoreCase("host")
                    || name.equalsIgnoreCase("connection")
                    || name.equalsIgnoreCase("user-agent")) {
                continue;
            }

            Enumeration<String> values = request.getHeaders(name);

            if (values != null && values.hasMoreElements()) {
                headerKey = name;
                break;
            }
        }

        String selectedName = Resolver.resolve(headerKey);

        File targetFile = new File("/srv/storage", selectedName);

        response.getWriter().println(
                "Access to file: '" + targetFile.toString() + "' created."
        );

        if (targetFile.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static class Resolver {

        public static String resolve(String value) {

            String result = "default.txt";

            HashMap<String, Object> container = new HashMap<>();

            container.put("alpha", "default.txt");
            container.put("beta", value);
            container.put("gamma", "placeholder.txt");

            container.put("result", container.get("alpha"));

            result = (String) container.get("result");

            return result;
        }
    }
}