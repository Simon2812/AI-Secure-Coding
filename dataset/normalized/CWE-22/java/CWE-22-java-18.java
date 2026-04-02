import java.io.File;
import java.io.IOException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ArchiveCheck {

    public void run(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        RequestAdapter adapter = new RequestAdapter(request);
        String value = adapter.read("item");
        if (value == null) {
            value = "";
        }

        String entry = new Switcher().convert(request, value);

        File base = new File("/srv/archive/items/");
        File target = new File(base, entry);

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private class Switcher {

        public String convert(HttpServletRequest request, String input) throws IOException {

            String result;
            String key = "ABC";
            char c = key.charAt(2);

            switch (c) {
                case 'A':
                    result = input;
                    break;
                case 'B':
                    result = "default";
                    break;
                case 'C':
                case 'D':
                    result = input;
                    break;
                default:
                    result = "default";
                    break;
            }

            return result;
        }
    }
}