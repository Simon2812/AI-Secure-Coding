import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FileLocationChecker {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String discovered = "";
        boolean searching = true;

        Enumeration<String> parameterNames = request.getParameterNames();

        while (parameterNames.hasMoreElements() && searching) {

            String key = parameterNames.nextElement();
            String[] values = request.getParameterValues(key);

            if (values != null) {

                for (int i = 0; i < values.length && searching; i++) {

                    String current = values[i];

                    if (current.equals("trigger")) {
                        discovered = key;
                        searching = false;
                    }
                }
            }
        }

        String selected = "";

        if (discovered != null) {

            List<String> container = new ArrayList<>();
            container.add("placeholder");
            container.add(discovered);
            container.add("constant");

            container.remove(0);

            selected = container.get(0);
        }

        File storageRoot = new File("/srv/storage/");
        File fileRef = new File(storageRoot, selected);

        response.getWriter().println("Access to file: '" + fileRef.toString() + "' created.");

        if (fileRef.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }
}