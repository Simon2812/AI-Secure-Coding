import java.io.File;
import java.io.IOException;
import java.util.Enumeration;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FileDirectoryProbe {

    public void execute(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String selected = "";
        boolean found = true;

        Enumeration<String> parameters = request.getParameterNames();

        while (parameters.hasMoreElements() && found) {

            String key = parameters.nextElement();
            String[] values = request.getParameterValues(key);

            if (values != null) {
                for (int i = 0; i < values.length && found; i++) {
                    String v = values[i];
                    if (v.equals("trigger")) {
                        selected = key;
                        found = false;
                    }
                }
            }
        }

        String directory = transform(selected);

        File fileRef = new File(directory, "Test.txt");

        response.getWriter().println("Access to file: '" + fileRef.toString() + "' created.");

        if (fileRef.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static String transform(String value) throws IOException {

        Processor processor = ProcessorFactory.create();
        String result = processor.apply(value);

        return result;
    }
}