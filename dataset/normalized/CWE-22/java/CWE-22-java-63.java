import java.io.FileInputStream;
import java.io.IOException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FilePreviewService {

    public void execute(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String input = request.getParameter("path");
        if (input == null) {
            input = "";
        }

        String selected;

        String seed = "ABC";
        char selector = seed.charAt(1); // always 'B'

        switch (selector) {

            case 'A':
                selected = input;
                break;

            case 'B':
                selected = "notes.txt";
                break;

            case 'C':
            case 'D':
                selected = input;
                break;

            default:
                selected = "default.txt";
                break;
        }

        String location = null;
        FileInputStream stream = null;

        try {

            location = "/srv/storage/" + selected;
            stream = new FileInputStream(location);

            byte[] buffer = new byte[1000];
            int size = stream.read(buffer);

            response.getWriter().println("The beginning of file: '" + location + "' is:\n\n");
            response.getWriter().println(new String(buffer, 0, size));

        } catch (Exception e) {

            System.out.println("Failed to open file: '" + location + "'");

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