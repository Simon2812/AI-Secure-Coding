import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ArchiveLookup {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String headerValue = "";
        if (request.getHeader("X-Archive") != null) {
            headerValue = request.getHeader("X-Archive");
        }

        headerValue = URLDecoder.decode(headerValue, StandardCharsets.UTF_8.name());

        String entry = new Processor().transform(request, headerValue);

        File base = new File("/opt/archive/");
        File target = new File(base, entry);

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private class Processor {

        public String transform(HttpServletRequest request, String value) throws IOException {

            Handler handler = HandlerFactory.create();
            String result = handler.handle(value);

            return result;
        }
    }
}