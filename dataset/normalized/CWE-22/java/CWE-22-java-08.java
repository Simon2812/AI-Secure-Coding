import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class DataFileCheck {

    public void execute(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String key = "";
        boolean searching = true;

        Enumeration<String> params = request.getParameterNames();
        while (params.hasMoreElements() && searching) {

            String current = params.nextElement();
            String[] values = request.getParameterValues(current);

            if (values != null) {
                for (int i = 0; i < values.length && searching; i++) {
                    String v = values[i];

                    if (v.equals("trigger")) {
                        key = current;
                        searching = false;
                    }
                }
            }
        }

        String name = "";
        if (key != null) {

            List<String> items = new ArrayList<>();
            items.add("safe");
            items.add(key);
            items.add("backup");

            items.remove(0);

            name = items.get(0);
        }

        File base = new File("/data/app/storage/");
        File file = new File(base, name);

        response.getWriter().println("Access to file: '" + file.toString() + "' created.");

        if (file.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }
}