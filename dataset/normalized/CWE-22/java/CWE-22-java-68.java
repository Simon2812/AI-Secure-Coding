import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class UriFileProbe {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        Cookie[] cookies = request.getCookies();

        String input = "none";
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("recent".equals(cookie.getName())) {
                    input = URLDecoder.decode(cookie.getValue(), StandardCharsets.UTF_8.name());
                    break;
                }
            }
        }

        String chosen = new Resolver().resolve(input);

        String uriPrefix = "";
        if (System.getProperty("os.name").contains("Windows")) {
            uriPrefix = "/";
        }

        try {

            URI uri = new URI(
                    "file:"
                            + uriPrefix
                            + "/srv/storage/"
                            .replace('\\', '/')
                            .replace(' ', '_')
                            + chosen
            );

            File fileRef = new File(uri);

            response.getWriter().println("Access to file: '" + fileRef.toString() + "' created.");

            if (fileRef.exists()) {
                response.getWriter().println(" And file already exists.");
            } else {
                response.getWriter().println(" But file doesn't exist yet.");
            }

        } catch (URISyntaxException e) {
            throw new IOException(e);
        }
    }

    private static class Resolver {

        public String resolve(String value) {

            int marker = 106;

            String result = (7 * 18) + marker > 200 ? "report.txt" : value;

            return result;
        }
    }
}