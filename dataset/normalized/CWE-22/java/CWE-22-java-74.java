import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ResourceCheckService {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        Cookie[] cookies = request.getCookies();

        String inputValue = "none";

        if (cookies != null) {
            for (Cookie c : cookies) {
                if (c.getName().equals("resource")) {
                    inputValue = URLDecoder.decode(c.getValue(), StandardCharsets.UTF_8.name());
                    break;
                }
            }
        }

        String selectedName = Resolver.resolve(inputValue);

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

            String result;

            String marker = "ABC";
            char branch = marker.charAt(1);

            switch (branch) {

                case 'A':
                    result = value;
                    break;

                case 'B':
                    result = "default.txt";
                    break;

                case 'C':
                case 'D':
                    result = value;
                    break;

                default:
                    result = "default.txt";
                    break;
            }

            return result;
        }
    }
}