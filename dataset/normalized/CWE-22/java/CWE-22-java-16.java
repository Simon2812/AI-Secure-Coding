import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ResourceInspector {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        Map<String,String[]> parameters = request.getParameterMap();

        String input = "";
        if (!parameters.isEmpty()) {
            String[] values = parameters.get("resource");
            if (values != null) {
                input = values[0];
            }
        }

        String name = new Transformer().apply(request, input);

        String prefix = "";
        if (System.getProperty("os.name").contains("Windows")) {
            prefix = "/";
        } else {
            prefix = "//";
        }

        try {

            URI uri = new URI(
                    "file",
                    null,
                    prefix + "/srv/app/data/".replace('\\', File.separatorChar).replace(' ', '_') + name,
                    null,
                    null
            );

            File target = new File(uri);

            response.getWriter().println("Access to file: '" + target.toString() + "' created.");

            if (target.exists()) {
                response.getWriter().println(" And file already exists.");
            } else {
                response.getWriter().println(" But file doesn't exist yet.");
            }

        } catch (URISyntaxException e) {
            throw new IOException(e);
        }
    }

    private class Transformer {

        public String apply(HttpServletRequest request, String value) throws IOException {

            String result = "";

            if (value != null) {

                List<String> list = new ArrayList<>();
                list.add("safe");
                list.add(value);
                list.add("backup");

                list.remove(0);

                result = list.get(0);
            }

            return result;
        }
    }
}