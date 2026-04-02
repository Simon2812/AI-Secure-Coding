import java.io.File;
import java.io.IOException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class DocumentLocator {

    public void handle(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String[] values = request.getParameterValues("path");
        String input;

        if (values != null && values.length > 0) {
            input = values[0];
        } else {
            input = "";
        }

        String directory = new Router().route(request, input);

        File target = new File(directory, "Test.txt");

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private class Router {

        public String route(HttpServletRequest request, String value) throws IOException {

            String result;
            String seed = "ABC";
            char selector = seed.charAt(2);

            switch (selector) {
                case 'A':
                    result = value;
                    break;
                case 'B':
                    result = "default";
                    break;
                case 'C':
                case 'D':
                    result = value;
                    break;
                default:
                    result = "default";
                    break;
            }

            return result;
        }
    }
}