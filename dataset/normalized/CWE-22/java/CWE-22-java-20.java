import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ResourceLookup {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String query = request.getQueryString();
        String key = "resource=";
        int pos = -1;

        if (query != null) {
            pos = query.indexOf(key);
        }

        if (pos == -1) {
            response.getWriter().println("Parameter not found.");
            return;
        }

        String raw = query.substring(pos + key.length());

        int amp = query.indexOf("&", pos);
        if (amp != -1) {
            raw = query.substring(pos + key.length(), amp);
        }

        raw = URLDecoder.decode(raw, StandardCharsets.UTF_8.name());

        String name = new Processor().handle(request, raw);

        File root = new File("/srv/files/");
        File target = new File(root, name);

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private class Processor {

        public String handle(HttpServletRequest request, String input) throws IOException {

            Handler handler = HandlerFactory.create();
            String result = handler.apply(input);

            return result;
        }
    }
}