import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class DocumentPreviewService {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        Map<String, String[]> parameters = request.getParameterMap();

        String userInput = "";
        if (!parameters.isEmpty()) {
            String[] values = parameters.get("path");
            if (values != null) {
                userInput = values[0];
            }
        }

        String selected;

        int marker = 86;

        if ((7 * 42) - marker > 200) {
            selected = "summary.txt";
        } else {
            selected = userInput;
        }

        String location = null;
        FileInputStream stream = null;

        try {

            location = "/srv/storage/" + selected;
            stream = new FileInputStream(new File(location));

            byte[] buffer = new byte[1000];
            int size = stream.read(buffer);

            response.getWriter().println("The beginning of file: '" + location + "' is:\n\n"
                    + new String(buffer, 0, size));

        } catch (Exception e) {

            System.out.println("Unable to open file: '" + location + "'");
            response.getWriter().println("Problem reading file: " + e.getMessage());

        } finally {

            if (stream != null) {
                try {
                    stream.close();
                    stream = null;
                } catch (Exception e) {
                }
            }
        }
    }
}