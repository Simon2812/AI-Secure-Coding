import java.io.File;
import java.io.IOException;
import java.util.Enumeration;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class DirectoryProbe {

    public void execute(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String candidate = "";
        boolean searching = true;

        Enumeration<String> params = request.getParameterNames();

        while (params.hasMoreElements() && searching) {

            String key = params.nextElement();
            String[] values = request.getParameterValues(key);

            if (values != null) {
                for (int i = 0; i < values.length && searching; i++) {

                    String v = values[i];

                    if (v.equals("trigger")) {
                        candidate = key;
                        searching = false;
                    }
                }
            }
        }

        String entry = new Adapter().map(request, candidate);

        File root = new File("/srv/storage/data/");
        File target = new File(root, entry);

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private class Adapter {

        public String map(HttpServletRequest request, String input) throws IOException {

            Handler handler = HandlerFactory.create();
            String result = handler.handle(input);

            return result;
        }
    }
}