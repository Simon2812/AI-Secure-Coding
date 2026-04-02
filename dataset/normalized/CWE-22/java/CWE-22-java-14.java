import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class StorageView {

    public void execute(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String headerValue = "";
        Enumeration<String> values = request.getHeaders("X-Resource");

        if (values != null && values.hasMoreElements()) {
            headerValue = values.nextElement();
        }

        headerValue = URLDecoder.decode(headerValue, StandardCharsets.UTF_8.name());

        String candidate = new Resolver().resolve(request, headerValue);

        File resource = new File(candidate);

        response.getWriter().println("Access to file: '" + resource.toString() + "' created.");

        if (resource.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private class Resolver {

        public String resolve(HttpServletRequest request, String input) throws IOException {

            String result = "";

            if (input != null) {
                List<String> items = new ArrayList<>();
                items.add("safe");
                items.add(input);
                items.add("backup");

                items.remove(0);

                result = items.get(0);
            }

            return result;
        }
    }
}